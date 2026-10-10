#!/usr/bin/env python3
"""Python ile çizilen, büyüyerek açılan bir buket.

Çalıştır: python3 cicek-buketi.py
Python standart kütüphanesi yeterlidir. SVG çizimini ve CSS animasyonunu
üretir, HTML dosyasını tarayıcıda açar. Aynı dosya telefonda da çalışır.
Yalnızca HTML üretmek için: python3 cicek-buketi.py --no-open
"""
from pathlib import Path
import argparse
import html
import math
import webbrowser


def tag(name, content='', **attrs):
    attributes = ' '.join(f'{k.replace("_", "-")}="{html.escape(str(v), quote=True)}"'
                          for k, v in attrs.items())
    return f'<{name} {attributes}>{content}</{name}>'


def path(d, fill='none', **attrs):
    return tag('path', d=d, fill=fill, **attrs)


def ellipse(x, y, rx, ry, color, angle=0):
    return tag('ellipse', cx=f'{x:.2f}', cy=f'{y:.2f}', rx=f'{rx:.2f}',
               ry=f'{ry:.2f}', fill=color, transform=f'rotate({angle:.2f} {x:.2f} {y:.2f})')


def circle(x, y, radius, color):
    return ellipse(x, y, radius, radius, color)


def petal(length, breadth, color, angle, rounded=False, vein=False):
    if rounded:
        drawing = ellipse(0, -length*.52, breadth, length*.55, color)
    else:
        drawing = path(f'M 0,5 C {-breadth:.2f},{-length*.2:.2f} '
                       f'{-breadth*.75:.2f},{-length*.85:.2f} 0,{-length:.2f} '
                       f'C {breadth*.75:.2f},{-length*.85:.2f} {breadth:.2f},{-length*.2:.2f} 0,5 Z', color)
    if vein:
        drawing += path(f'M 0,0 Q -3,{-length*.5:.2f} 0,{-length*.85:.2f}',
                        stroke='#fff2db', stroke_width='.8', opacity='.26')
    return tag('g', drawing, transform=f'rotate({angle:.2f})')


def radial(count, length, breadth, colors, offset=0, rounded=False, vein=False):
    return ''.join(petal(length, breadth, colors[i % len(colors)],
                         i*360/count+offset, rounded, vein) for i in range(count))


def stamens(r, count=14, dark='#5b3533', gold='#ebc778'):
    drawing = circle(0, 0, r*.22, dark)
    for i in range(count):
        a = i*math.tau/count
        x, y = math.cos(a)*r*.32, math.sin(a)*r*.32
        drawing += path(f'M 0,0 L {x:.2f},{y:.2f}', stroke=dark, stroke_width='1.3')
        drawing += circle(x, y, r*.032, gold)
    return drawing


def flower(kind, r):
    if kind == 'daisy':
        return radial(17,r,r*.19,['#fff9e9','#e5e6de','#fff4dc'],vein=True) + circle(0,0,r*.24,'#d5a82c') + circle(-2,-2,r*.13,'#f4d16e')
    if kind == 'sunflower':
        drawing = radial(21,r,r*.21,['#eaa52b','#f4c84f','#d58c1c'])
        drawing += radial(16,r*.87,r*.16,['#ffdc65','#eebb3c'],10)
        drawing += circle(0,0,r*.40,'#4c3227')
        for i in range(76):
            a=i*2.399963; q=math.sqrt(i/76)*r*.35
            drawing += circle(math.cos(a)*q,math.sin(a)*q,r*.017,'#d1a55c' if i%2 else '#ae8148')
        return drawing
    if kind == 'tulip':
        drawing = petal(r*1.20,r*.70,'#b74567',-27,vein=True)
        drawing += petal(r*1.20,r*.70,'#f5a0ad',27,vein=True)
        drawing += petal(r*1.03,r*.74,'#e87896',0,vein=True)
        return tag('g',drawing,transform=f'translate(0 {r*.25})')
    if kind == 'poppy':
        drawing = radial(5,r,r*.55,['#d94840','#ef7056','#f28469'],17,True,True)
        return drawing + stamens(r,18,'#332d31','#e6c49a')
    if kind == 'lavender':
        drawing = path(f'M 0,8 L 0,{-r*2.7}',stroke='#6c8c57',stroke_width='2')
        for i in range(10):
            y=-i*r*.25; b=r*.31*(1-i*.055)
            drawing += ellipse(-b*.8,y,b,b*.57,['#a892cd','#8971b8'][i%2],27)
            drawing += ellipse(b*.8,y-r*.08,b,b*.57,['#c5b0df','#ac92d0'][i%2],-27)
        return drawing + ellipse(0,-r*2.65,r*.13,r*.22,'#d8c7e9')
    if kind == 'lily':
        drawing = radial(3,r,r*.42,['#d6aec5','#efd8e4','#e8c9d9'],20,vein=True)
        drawing += radial(3,r*.99,r*.30,['#fff3e9','#efdee3','#fff2ed'],80,vein=True)
        for i in range(5):
            a=(i-2)*.35; x=math.sin(a)*r*.44; y=-math.cos(a)*r*.44
            drawing += path(f'M 0,3 L {x},{y}',stroke='#9aa759',stroke_width='1.1')
            drawing += ellipse(x,y,r*.035,r*.083,'#be8043',a*180/math.pi)
        return drawing
    if kind in ('rose','peony'):
        colors = ['#a33158','#cc5478','#ef8aa6','#ffc0c8'] if kind=='rose' else ['#ce6588','#e894ad','#f3b8c4','#ffdad9']
        drawing = ''
        for layer,(count,size,breadth) in enumerate([(9,1,.53),(8,.79,.50),(7,.60,.44),(6,.40,.32)]):
            drawing += radial(count,r*size,r*breadth,[colors[layer],colors[min(layer+1,3)]],layer*21,True,True)
        return drawing + ellipse(0,0,r*.13,r*.1,'#b74e73',-30)
    if kind in ('cosmos','zinnia','chrysanthemum'):
        if kind=='cosmos':
            return radial(8,r,r*.30,['#af4e87','#d67cad','#e995b8'],12,True,True)+stamens(r,13,'#c49a38','#f7dda0')
        if kind=='zinnia':
            drawing = ''
            for i in range(4):
                drawing += radial(12+i*2,r*(1-i*.17),r*.24,['#df8751','#f2aa69','#f7c080'],i*14,True,True)
            return drawing+circle(0,0,r*.12,'#b77437')
        drawing = ''
        for i in range(4):
            drawing += radial(23,r*(1-i*.17),r*.09,['#f1e2ad','#fff3cc','#cdbc85'],i*8,vein=True)
        return drawing+circle(0,0,r*.09,'#d8b96c')
    if kind == 'anemone':
        return radial(9,r,r*.36,['#bbadd6','#d6c8e6','#e8dbee'],10,True,True)+stamens(r,28,'#2d3045','#74728e')
    if kind in ('hydrangea','forgetmenot'):
        drawing=''; count=29 if kind=='hydrangea' else 11
        for i in range(count):
            a=i*2.399963; q=math.sqrt(i/count)*r*.78
            x=math.cos(a)*q; y=math.sin(a)*q
            small=r*(.19 if kind=='hydrangea' else .24)
            colors=['#91b6d1','#b3cce0','#748fbf','#c3d5e5'] if kind=='hydrangea' else ['#7db6ce','#a4d2df','#70a0c7']
            f=radial(4 if kind=='hydrangea' else 5,small,small*.45,colors,i*23,True)
            f+=circle(0,0,small*.16,'#e9d795')
            drawing+=tag('g',f,transform=f'translate({x:.2f} {y:.2f})')
        return drawing
    if kind == 'orchid':
        drawing = radial(3,r,r*.39,['#9f609f','#c999cb','#e1bce1'],60,True,True)
        drawing += petal(r*.92,r*.52,'#e5c5e4',-62,True,True)+petal(r*.92,r*.52,'#bd86c0',62,True,True)
        drawing += ellipse(0,r*.28,r*.22,r*.31,'#f1d9eb')+ellipse(0,r*.32,r*.1,r*.18,'#8e457e')
        return drawing + circle(0,0,r*.09,'#f2d892')
    if kind == 'iris':
        drawing=radial(3,r*.8,r*.25,['#8b81be','#a197d0','#bdb1dc'],0,True,True)
        drawing+=radial(3,r,r*.36,['#6864a5','#8278b8','#8f85c1'],60,True,True)
        drawing+=radial(3,r*.46,r*.09,['#e5c778'],60)
        return drawing
    if kind == 'snapdragon':
        drawing=path(f'M 0,8 L 0,{-r*2.7}',stroke='#759665',stroke_width='2')
        for i in range(8):
            y=-i*r*.3; s=r*.32*(1-i*.065)
            f=ellipse(-s*.7,-s*.2,s,s*.65,'#e8a798')+ellipse(s*.7,-s*.2,s,s*.65,'#f3b9a3')+ellipse(0,s*.3,s*.6,s*.55,'#f8d5b4')
            drawing+=tag('g',f,transform=f'translate({(-1 if i%2 else 1)*s*.5} {y})')
        return drawing
    raise ValueError(kind)


# Tür, çiçek merkezi, boyut. Başlar yakın, saplar aynı dar bölgede birleşir.
PLANTS = [
    ('lavender',305,333,31),('snapdragon',630,294,28),('iris',699,375,48),
    ('sunflower',437,323,61),('daisy',364,413,42),('peony',549,383,58),
    ('hydrangea',315,482,54),('tulip',459,444,41),('lily',637,459,57),
    ('orchid',254,552,45),('rose',409,526,55),('cosmos',551,522,48),
    ('poppy',706,557,43),('anemone',485,595,44),
    ('chrysanthemum',359,611,47),('zinnia',582,615,45),('forgetmenot',286,626,32),
]


def bezier(points,t):
    a,b,c,d=points; u=1-t
    return (u*u*u*a[0]+3*u*u*t*b[0]+3*u*t*t*c[0]+t*t*t*d[0],
            u*u*u*a[1]+3*u*u*t*b[1]+3*u*t*t*c[1]+t*t*t*d[1])


def leaf(x,y,length,angle,delay,color):
    drawing=path(f'M 0,0 C {length*.18},{-length*.48} {length*.75},{-length*.55} {length},0 '
                 f'C {length*.68},{length*.31} {length*.2},{length*.24} 0,0 Z',color)
    drawing+=path(f'M 0,0 Q {length*.45},-6 {length*.9},0',stroke='#8caa79',stroke_width='.8',opacity='.45')
    inner=tag('g',drawing,**{'class':'leaf-grow','style':f'--delay:{delay:.2f}s'})
    return tag('g',inner,transform=f'translate({x:.2f} {y:.2f}) rotate({angle})')


def plant(index,description):
    kind,x,y,r=description
    base=500+(index%5-2)*7
    delay=(index*1.31)%2.3
    points=((base,868),(base+(x-500)*.16,731),(x+(500-x)*.13,y+121),(x,y))
    a,b,c,d=points
    curve=f'M {a[0]},{a[1]} C {b[0]},{b[1]} {c[0]},{c[1]} {d[0]},{d[1]}'
    drawing=path(curve,stroke='#4b754b',stroke_width=3.8 if kind in ('sunflower','peony') else 2.6,
                 stroke_linecap='round',pathLength='1',**{'class':'stem','style':f'--delay:{delay:.2f}s'})
    for i,t in enumerate((.45,.61,.77)):
        lx,ly=bezier(points,t)
        angle=-38 if (i+index)%2 else -145
        drawing+=leaf(lx,ly,40+(index+i)%4*9,angle,delay+1.5+t*3.2,['#355e49','#49785b','#5d865f'][(i+index)%3])
    head=tag('g',flower(kind,r),**{'class':'flower-head','style':f'--delay:{delay+5.1:.2f}s'})
    drawing+=tag('g',head,transform=f'translate({x} {y}) rotate({(index%3-1)*8})')
    return tag('g',drawing,**{'class':'plant','style':f'--sway-delay:{-index*.59:.2f}s'})


def fillers():
    drawing=''
    for branch,(x,y) in enumerate([(242,442),(748,476),(254,635),(733,632),(548,260)]):
        delay=1+branch*.21
        drawing+=path(f'M 500,848 Q {x},680 {x},{y}',stroke='#718a6b',stroke_width='1.2',
                      pathLength='1',**{'class':'stem','style':f'--delay:{delay}s'})
        for i in range(9):
            a=i*2.399; q=math.sqrt(i/9)*26
            bx=x+math.cos(a)*q; by=y+math.sin(a)*q
            drawing+=path(f'M {x},{y+35} L {bx},{by}',stroke='#719171',stroke_width='.8',
                          opacity='.8',**{'class':'filler','style':f'--delay:{delay+4.1}s'})
            tiny=''.join(circle(math.cos(j*math.tau/5)*2,math.sin(j*math.tau/5)*2,2.2,'#f5eddb') for j in range(5))
            drawing+=tag('g',tag('g',tiny,**{'class':'flower-head','style':f'--delay:{delay+5+i*.05}s'}),transform=f'translate({bx} {by})')
    return drawing


def bouquet_svg():
    defs='''<defs>
      <radialGradient id="halo"><stop stop-color="#516445" stop-opacity=".24"/><stop offset="1" stop-color="#14211f" stop-opacity="0"/></radialGradient>
      <linearGradient id="paper" x2="1" y2="1"><stop stop-color="#c9b998"/><stop offset=".5" stop-color="#a7997a"/><stop offset="1" stop-color="#786e59"/></linearGradient>
      <linearGradient id="front" x2="1" y2=".7"><stop stop-color="#decdac"/><stop offset=".5" stop-color="#b5a587"/><stop offset="1" stop-color="#9a8a70"/></linearGradient>
      <linearGradient id="soil" x2="0" y2="1"><stop stop-color="#33392b"/><stop offset="1" stop-color="#101c1b"/></linearGradient>
    </defs>'''
    scene=defs+ellipse(500,450,320,365,'url(#halo)')
    for i in range(23):
        scene+=circle(200+(i*83)%600,200+(i*137)%690,1,'#707c68')
    scene+=path('M 155,924 Q 335,891 510,923 Q 705,894 845,926 L 845,1000 L 155,1000 Z','url(#soil)')
    # Arkadaki iki kâğıt kanadı, buketin ağzını geniş tutar.
    scene+=path('M 280,616 L 474,725 L 642,604 L 586,873 L 470,922 Z','#857b63')
    scene+=path('M 293,610 L 500,770 L 668,633 L 554,928 L 475,925 Z','url(#paper)')
    scene+=path('M 280,616 L 474,725 L 642,604',stroke='#cbbc9c',stroke_width='1.3')
    # Çiçeklerin arkasında büyüyen okaliptüs dalları.
    for branch,(x,y) in enumerate([(295,454),(720,504),(357,320),(669,349)]):
        scene+=path(f'M 500,856 Q {x},700 {x},{y}',stroke='#507562',stroke_width='2',pathLength='1',
                    **{'class':'stem','style':f'--delay:{branch*.34}s'})
        for j in range(6):
            f=j/6; yy=y+f*210; xx=x+(500-x)*f*f*.45
            for side in (-1,1):
                shape=ellipse(side*15,-5,19-j*.9,12-j*.4,['#527f76','#668d7e','#39675e'][j%3],side*30)
                scene+=tag('g',tag('g',shape,**{'class':'leaf-grow','style':f'--delay:{2+j*.25+branch*.3}s'}),transform=f'translate({xx} {yy})')
    scene+=fillers()
    for index,p in enumerate(PLANTS):
        scene+=plant(index,p)
    # Ön kâğıt sapları toplar; üstteki bütün çiçek başları açıkta kalır.
    scene+=path('M 335,693 Q 418,726 506,802 L 663,671 L 556,925 L 486,938 Z','url(#front)')
    scene+=path('M 335,693 Q 418,726 506,802 L 486,938',stroke='#e4d4b5',stroke_width='1.4',opacity='.65')
    scene+=path('M 506,802 L 556,925',stroke='#7d715b',stroke_width='1.2',opacity='.4')
    scene+=path('M 462,855 Q 503,874 584,848 L 578,866 Q 512,893 468,876 Z','#8e5362')
    scene+=path('M 525,870 C 478,823 441,841 487,870 C 503,879 518,875 525,870 Z','#aa6978')
    scene+=path('M 525,870 C 562,820 602,827 569,862 C 554,878 535,878 525,870 Z','#bd8190')
    scene+=path('M 522,873 Q 488,913 479,938 L 500,928 L 508,941 Q 514,906 529,879 Z','#a76676')
    scene+=path('M 531,875 Q 561,907 570,941 L 552,929 L 544,941 Q 544,906 525,878 Z','#bb7b88')
    scene+=ellipse(526,872,9,8,'#7b4354',-16)
    return tag('svg',scene,xmlns='http://www.w3.org/2000/svg',viewBox='175 165 650 815',
               role='img',aria_label='Dar bir noktadan filizlenerek büyüyen, 17 farklı çiçek ve cipsofilyadan oluşan dolgun buket.')


def build_document():
    return '''<!doctype html>
<html lang="tr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="theme-color" content="#101c1b"><meta name="description" content="Birlikte büyüyüp açılan rengârenk bir buket.">
<title>Birlikte çiçek açalım</title>
<style>
*{box-sizing:border-box} :root{color-scheme:dark;font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;background:#101c1b;color:#eee6d2}
body{margin:0;height:100svh;min-height:510px;display:flex;flex-direction:column;background:radial-gradient(ellipse at 50% 48%,#1a2b25 0%,#101c1b 68%)}
header{text-align:center;padding:25px 16px 4px}.eyebrow{font-size:10px;letter-spacing:.30em;color:#a0af97;margin:0 0 10px}
h1{font:400 clamp(26px,4vw,36px) Georgia,serif;letter-spacing:-.025em;margin:0}
main{flex:1;min-height:220px;width:100%;display:flex;justify-content:center;min-width:0;padding:0 10px}
.stage{width:min(100%,800px);height:100%;min-height:0;position:relative}.stage svg{width:100%;height:100%;display:block;overflow:hidden}
footer{text-align:center;padding:4px 12px 22px;color:#aebb9e}footer p{font-size:11px;letter-spacing:.07em;margin:0 0 13px}
.controls{display:flex;justify-content:center;gap:10px;align-items:center}.controls form{margin:0}
button,.pause-label{border:1px solid #58634e;background:#1b2c23;color:#dfdfc8;border-radius:24px;padding:10px 17px;min-height:41px;font:12px -apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;cursor:pointer;display:inline-flex;align-items:center;gap:7px}
button:hover,.pause-label:hover{background:#2c3d2d}button:focus-visible,input:focus-visible{outline:2px solid #edcea1;outline-offset:4px}input{accent-color:#aab898;width:14px;height:14px;margin:0}
.stem{stroke-dasharray:1;stroke-dashoffset:1;animation:grow 5.2s cubic-bezier(.33,.01,.35,1) var(--delay) both}
.flower-head{transform-origin:0 0;animation:bloom 1.9s cubic-bezier(.22,.75,.25,1) var(--delay) both}
.leaf-grow{transform-origin:0 0;animation:leaf 1.7s cubic-bezier(.22,.75,.25,1) var(--delay) both}
.filler{animation:appear 1.3s ease var(--delay) both}.plant{transform-origin:500px 868px;animation:sway 7s ease-in-out var(--sway-delay) infinite alternate}
body:has(#pause:checked) .stage *{animation-play-state:paused!important}
@keyframes grow{from{stroke-dashoffset:1}to{stroke-dashoffset:0}}@keyframes bloom{0%{transform:rotate(-18deg) scale(.001);opacity:0}30%{opacity:1}100%{transform:rotate(0) scale(1);opacity:1}}
@keyframes leaf{from{transform:scale(.001);opacity:0}to{transform:scale(1);opacity:1}}@keyframes appear{from{opacity:0}to{opacity:.8}}@keyframes sway{from{transform:rotate(-.25deg)}to{transform:rotate(.25deg)}}
@media(prefers-reduced-motion:reduce){.stage *{animation:none!important}.stem{stroke-dashoffset:0}}
@media(max-width:540px){header{padding-top:22px}.eyebrow{font-size:9px}main{padding:0 2px}footer{padding-bottom:24px}}
</style></head><body>
<header><p class="eyebrow">HER BİRİ BAŞKA · HEPSİ BİR ARADA</p><h1>Birlikte çiçek açalım.</h1></header>
<main><div class="stage">''' + bouquet_svg() + '''</div></main>
<footer><p>Bir filizden, rengârenk bir bukete.</p><div class="controls">
<form method="get"><button type="submit" name="yeniden" value="1">Yeniden büyüt</button></form>
<label class="pause-label"><input type="checkbox" id="pause">Duraklat</label>
</div></footer></body></html>
'''


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--no-open',action='store_true',help='Tarayıcıyı açmadan HTML oluştur.')
    parser.add_argument('--output',type=Path,help='HTML çıktı yolu.')
    args=parser.parse_args()
    output=args.output or Path(__file__).with_name('cicek-bahcesi.html')
    output.write_text(build_document(),encoding='utf-8')
    print(f'Buket hazır: {output.resolve()}')
    if not args.no_open:
        webbrowser.open(output.resolve().as_uri())


if __name__=='__main__':
    main()
