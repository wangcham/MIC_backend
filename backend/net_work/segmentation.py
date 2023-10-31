import torch
import os
from torch import nn
from torch.nn import functional as F
from PIL import Image
from torchvision import transforms
from torchvision.utils import save_image
from flask import Flask
import config
import db
import datetime

class Conv_Block(nn.Module):
    def __init__(self, in_channel, out_channel):
        super(Conv_Block, self).__init__()
        self.layer = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, 3, 1, 1, padding_mode='reflect', bias=False),
            nn.BatchNorm2d(out_channel),
            nn.Dropout2d(0.3),
            nn.LeakyReLU(),
            nn.Conv2d(out_channel, out_channel, 3, 1, 1, padding_mode='reflect', bias=False),
            nn.BatchNorm2d(out_channel),
            nn.Dropout2d(0.3),
            nn.LeakyReLU()
        )

    def forward(self, x):
        return self.layer(x)


class DownSample(nn.Module):
    def __init__(self, channel):
        super(DownSample, self).__init__()
        self.layer = nn.Sequential(
            nn.Conv2d(channel, channel, 3, 2, 1, padding_mode='reflect', bias=False),
            nn.BatchNorm2d(channel),
            nn.LeakyReLU()
        )

    def forward(self, x):
        return self.layer(x)


class UpSample(nn.Module):
    def __init__(self, channel):
        super(UpSample, self).__init__()
        # 插值法
        self.layer = nn.Conv2d(channel, channel // 2, 1, 1)

    def forward(self, x, feature_map):
        up = F.interpolate(x, scale_factor=2, mode='nearest')
        out = self.layer(up)
        return torch.cat((out, feature_map), dim=1)


class UNet(nn.Module):
    def __init__(self):
        super(UNet, self).__init__()
        self.c1 = Conv_Block(3, 64)
        self.d1 = DownSample(64)
        self.c2 = Conv_Block(64, 128)
        self.d2 = DownSample(128)
        self.c3 = Conv_Block(128, 256)
        self.d3 = DownSample(256)
        self.c4 = Conv_Block(256, 512)
        self.d4 = DownSample(512)
        self.c5 = Conv_Block(512, 1024)

        self.u1 = UpSample(1024)
        self.c6 = Conv_Block(1024, 512)
        self.u2 = UpSample(512)
        self.c7 = Conv_Block(512, 256)
        self.u3 = UpSample(256)
        self.c8 = Conv_Block(256, 128)
        self.u4 = UpSample(128)
        self.c9 = Conv_Block(128, 64)
        self.out = nn.Conv2d(64, 3, 3, 1, 1)
        self.Th = nn.Sigmoid()

    def forward(self, x):
        R1 = self.c1(x)
        R2 = self.c2(self.d1(R1))
        R3 = self.c3(self.d2(R2))
        R4 = self.c4(self.d3(R3))
        R5 = self.c5(self.d4(R4))

        U1 = self.c6(self.u1(R5, R4))
        U2 = self.c7(self.u2(U1, R3))
        U3 = self.c8(self.u3(U2, R2))
        U4 = self.c9(self.u4(U3, R1))

        return self.Th(self.out(U4))


class Segmentation:
    def __init__(self, ori_path, weight_path):
        self.path = ori_path
        self.weight_path = weight_path
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print('传给算法的图像路径是'+self.path)
        self.img = Image.open(self.path)
        print("1", type(self.img)) 
        transform = transforms.Compose([transforms.ToTensor()])
        self.img = transform(self.img)
        print("2",type(self.img))
        self.net = UNet()

    def work(self):
        if os.path.exists(self.weight_path):
            # self.net.load_state_dict(torch.load(self.weight_path),  map_location=torch.device('cpu'))
            self.net.load_state_dict(torch.load(self.weight_path))
        else:
            return "找不到参数文件，加载失败"
            # print("3", type(self.img))
            # print("4",type(self.img.unsqueese(0)))
        output = self.net(self.img.unsqueeze(0))
        print("5", type(output))
        return output

#运行主类
class operate:
    def run(self,img_path,patient_id):
        try:
            origin = os.path.dirname(os.path.abspath(__file__))

            self.weight_path =os.path.join(origin,'unet_params','cpu_weight.pth')
            print("路径："+self.weight_path)
            self.path1 = config.origin_path
            ori_path = img_path
            path2 = 'segmentation_image'
            #获取当前py文件所在目录
            origin = os.path.dirname(os.path.abspath(__file__))
            print(origin)
            path3 = os.path.join(origin,path2)
            print(path3)
            img_name = str(patient_id)+'.png'
            save_path = os.path.join(path3, img_name)
            print('保存的路径是'+save_path)
            
            first_person = Segmentation(ori_path=ori_path, weight_path=self.weight_path)
            
            #进行分割
            output = first_person.work()
            save_image(output, f'{save_path}')
            print("算法保存的图片位于"+save_path)

            database = db.Database()
        
            sql = """
            update patients set segpath = %s where id = %s
            """
            
            params = (save_path, int(patient_id))
            database.execute(sql,params)
            return "图片分割完成"
        except Exception as e:
            return str(e)
    
    def pubrun(self,img_path):
        try:
            origin = os.path.dirname(os.path.abspath(__file__))
            pth_path = os.path.join(origin,'unet_params','cpu_weight.pth')
            self.weight_path=pth_path
            print("路径："+self.weight_path)
            self.path1 = config.origin_path
            ori_path = img_path

            #进行合成文件名字操作
            img_name = get_current_time()+'.png'
            path2 = 'segmentation_image'
            origin = os.path.dirname(os.path.abspath(__file__))
            path3 = os.path.join(origin,path2)
            save_path = os.path.join(path3,img_name)
            #save_path是文件绝对路径
            first_person = Segmentation(ori_path=ori_path,weight_path=self.weight_path)

            output = first_person.work()
            print("36",type(output))
            save_image(output,f'{save_path}')
            print("分割之后的图片是"+save_path)
            return save_path
        except Exception as e:
            print(str(e))
            return str(e)


def get_current_time():
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')