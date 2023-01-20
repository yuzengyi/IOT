from machine import Pin,ADC
import time
import onewire
import ds18x20

#定义DS18B20控制对象
ds18b20=ds18x20.DS18X20(onewire.OneWire(Pin(13)))

light = 35

#雨滴传感器
TiltPin  = 26    # 传感器DO端口
ledpin   = 15    # LED端口
adcpin   = 34    # 传感器AO端口端口
n = 0

def setup():
    global light_ADC
    light_ADC = ADC(Pin(light))     
    light_ADC.atten(ADC.ATTN_11DB)  # 11dB 衰减, 最大输入电压约3.6v 
    global raind_ADC
    global raind_DO

    led = Pin(ledpin,Pin.OUT) # 设置LED管脚为输出模式
    raind_ADC = ADC(Pin(adcpin))        # ADC6复用管脚为GP34
    raind_ADC.atten(ADC.ATTN_11DB)      # 11dB 衰减, 最大输入电压约3.6v
    Tilt = Pin(TiltPin, Pin.IN, Pin.PULL_UP) # 设置为输入模式
    # 中断函数，调用call_back函数
    Tilt.irq(trigger=Pin.IRQ_FALLING,handler=call_back)
# 中断函数，模块切斜，响应中断函数
def call_back(Tilt):
    global n
    n=not n
    led.value(n)
#程序入口
if __name__=="__main__":
    roms = ds18b20.scan()  #扫描是否存在DS18B20设备
    print("DS18B20初始化成功！")
    setup()           # 初始化GPIO口
    status = 1 # 状态值
    while True:
        ds18b20.convert_temp()
        print ('光照强度: ', light_ADC.read()/4095.00*100,'%') # 读取ADC6的值16-bits，获取光敏模拟量值
        time.sleep(1)
        print ('湿度值：',(1-raind_ADC.read()/4095.00)*100,'%')  # 输出模拟信号值
        time.sleep(1)
        for rom in roms:
            print("DS18B20检测温度：%.2f°C" %ds18b20.read_temp(rom))
