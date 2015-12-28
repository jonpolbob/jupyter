import colorsys


def wav2RGB(wavelength):
    w = int(wavelength)

    # colour
    if w >= 380 and w < 440:
        R = -(w - 440.) / (440. - 350.)
        G = 0.0
        B = 1.0
    elif w >= 440 and w < 490:
        R = 0.0
        G = (w - 440.) / (490. - 440.)
        B = 1.0
    elif w >= 490 and w < 510:
        R = 0.0
        G = 1.0
        B = -(w - 510.) / (510. - 490.)
    elif w >= 510 and w < 580:
        R = (w - 510.) / (580. - 510.)
        G = 1.0
        B = 0.0
    elif w >= 580 and w < 645:
        R = 1.0
        G = -(w - 645.) / (645. - 580.)
        B = 0.0
    elif w >= 645 and w <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    # intensity correction
    if w >= 380 and w < 420:
        SSS = 0.3 + 0.7*(w - 350) / (420 - 350)
    elif w >= 420 and w <= 700:
        SSS = 1.0
    elif w > 700 and w <= 780:
        SSS = 0.3 + 0.7*(780 - w) / (780 - 700)
    else:
        SSS = 0.0
    SSS *= 255

    return [int(SSS*R), int(SSS*G), int(SSS*B)]


def rgbtonm(r,g,b):
    nm=0
    h,l,s = colorsys.rgb_to_hls(float(r)/255.0, float(g)/255.0, float(b)/255.0)
    h = h*255.0
    if h>128 :
        nm = 490 - (128-h)/(128-189)*(490-400)
    if h<=128 and h>85:
        nm = 510 - (85-h)/(85-128)*(510-490)
    if h<=85 and h>16:
        nm = 620 - (16-h)/(16-85)*(620-510)
    if h<=16 and h>=3:
        nm = 640 - (3-h)/(3-16)*(640-620)
        
    return h,nm

def rgbsta(r,g,b):
    h,l,s = colorsys.rgb_to_hls(float(r)/255.0, float(g)/255.0, float(b)/255.0)
    print 'hls', h,l,s
    outr,outg,outb = colorsys.hls_to_rgb(float(h), .5, 1.0)
    print 'rgb', outr,outg,outb
    return outr,outg,outb

def loopnm():
    for nm in range(400,800,10):
        r,g,b = wav2RGB(nm)
        h,resu = rgbtonm(r,g,b)
        print nm,h,resu
            
r = raw_input('red (0-255) ? ')
g = raw_input('green (0-255) ? ')
b = raw_input('blue (0-255) ? ')

#r,g,b = wav2RGB(nm)
h,resu = rgbtonm(r,g,b)

print 'estimated for','red=',int(r),' green:',int(g), ' blue :',int(b),'nm=', resu,'(hue = ',h,')'

rgbout = rgbsta(r,g,b)

print 'pure color RGBcomponents = ',[int(x*255.0) for x in rgbout]

raw_input()

