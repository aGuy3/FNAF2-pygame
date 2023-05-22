import pygame
from settings import *
from spritesheet import Spritesheet
import random
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption(TITLE)
pygame.display.get_desktop_sizes()
pygame.display.toggle_fullscreen()
windowIcon=pygame.image.load('windowIcon.jpg')
pygame.display.set_icon(windowIcon)
office=pygame.sprite.Group()
officeInts=pygame.sprite.Group()
officeDesks=pygame.sprite.Group()
sfx=pygame.sprite.Group()
player=pygame.sprite.Group()
camUI=pygame.sprite.Group()#Group for the UI in camera
cam=pygame.sprite.Sprite()#sprite for the camera sprites for the diffrent rooms
textCam=pygame.sprite.Sprite()#Sprite for the text that says the current room
static=pygame.sprite.Sprite()#Sprite static for camrea
mask=pygame.sprite.Sprite()#sprite for freddy mask
musicBox=pygame.sprite.Sprite()#sprite for musicbox timer on PRISECOUNTER camera
monitor=pygame.sprite.Sprite()#sprite for monitor closing/opening when opening cameras
white=pygame.sprite.Sprite()
flashlight=pygame.sprite.Sprite()


static.frame=0 #Frame number for static animation
monitor.frame=0 #Frame number for camera animation
white.frame=0 #Frame number for glitch when changing camreas
white.ani=False #if animation is happening
#PLAYER ATTRIBUTES
player.camsUp=False #if cameras are up/down
player.maskOn=False #if mask is on/off
player.C=0 #number to help use of mask button in onMouseMove
player.C2=0
player.currentCam='PRISECOUNTER' #keeps track of current camera that the player is on
player.flashbattery=100 #flashlight battery
player.dead=False
player.inMenu=False
def update():
    updateOffice()
    updateCams()
    PlayAmbience()
    syncMove(leftOff)
    syncMove(rightOff)
    syncMove(leftOn)
    syncMove(rightOn)
    syncMove(desk1)
    syncMove(desk2)
    syncMove(desk3)
    syncMove(desk4)
    syncMove(toyfreddy)
    syncMove(mangleO)
    syncMove(goldenfreddy)
    ToyBonnieJS()
    updateAi()
    Musicbox()
    
def updateOffice():
    
    if TC.pos=='OFFICE-HALLWAY' or TF.pos=='OFFICE-HALL1' or TF.pos=='OFFICE-HALL2' or WB.pos=='OFFICE-HALL' or WF.pos=='OFFICE-HALL' or MA.pos=='OFFICE-HALL' or WFO.pos=='OFFICE-HALL' or GF.pos=='OFFICE-HALL':
        office.hallfull=True
    else:
        office.hallfull=False
        sfx.ambiencescary.stop()
    
    if monitor.frame<=1 and GF.pos=='IN-OFFICE' or GF.pos=='OFFICE-HALL':
        GF.seen=True
    GF.timer+=1
    if GF.increase:
        GF.value+=1
    if WFO.ai>0:
        WFO.valueTimer+=1
        if office.inside==False and WFO.valueTimer>=30:
            WFO.value+=1
            WFO.valueTimer=0
    #Code for bonnie and chica in office 
    blackscreen.image.set_alpha(blackscreen.opacity)
    toybonnie.rect.x-=toybonnie.dx
    toychica.rect.x-=toychica.dx
    if office.inside:
        chance=random.randint(1,4)
        office.maskTime+=1
        if chance==2:
            blackscreen.opacity=0
        else:
            blackscreen.opacity=random.randint(200,255)
        if TB.pos=='IN-OFFICE':
            if toybonnie.rect.centerx<WIDTH/2+110:
                if office.side=='NONE':
                    toybonnie.dx=-10
                elif office.side=='LEFT':
                    toybonnie.dx=-35
                elif office.side=='RIGHT':
                    toybonnie.dx=15
            elif toybonnie.rect.centerx>WIDTH/2+120:
                if office.side=='NONE':
                    toybonnie.dx=10
                elif office.side=='RIGHT':
                    toybonnie.dx=35
                elif office.side=='LEFT':
                    toybonnie.dx=-15
            else:
                if office.side=='NONE':
                    toybonnie.dx=0
                elif office.side=='RIGHT':
                    toybonnie.dx=25
                elif office.side=='LEFT':
                    toybonnie.dx=-25
            if office.maskTime>120:
                blackscreen.opacity=255
                TB.pos='SHOWSTAGE'
                office.inside=False
        elif TC.pos=='IN-OFFICE':
            if toychica.rect.centerx<WIDTH/2-80:
                if office.side=='NONE':
                    toychica.dx=-10
                elif office.side=='LEFT':
                    toychica.dx=-35
                elif office.side=='RIGHT':
                    toychica.dx=15
            elif toychica.rect.centerx>WIDTH/2-70:
                if office.side=='NONE':
                    toychica.dx=10
                elif office.side=='RIGHT':
                    toychica.dx=35
                elif office.side=='LEFT':
                    toychica.dx=-15
            else:
                if office.side=='NONE':
                    toychica.dx=0
                elif office.side=='RIGHT':
                    toychica.dx=25
                elif office.side=='LEFT':
                    toychica.dx=-25
            if office.maskTime>120:
                blackscreen.opacity=255
                TC.pos='SHOWSTAGE'
                office.inside=False
        elif TF.pos=='IN-OFFICE':
            if office.maskTime>120:
                blackscreen.opacity=255
                TC.pos='SHOWSTAGE'
                office.inside=False
        elif WB.pos=='IN-OFFICE':
            if office.maskTime>120:
                blackscreen.opacity=255
                WB.pos='P&S'
                office.inside=False
        elif WC.pos=='IN-OFFICE':
            if office.maskTime>120:
                blackscreen.opacity=255
                WC.pos='P&S'
                office.inside=False
        elif WF.pos=='IN-OFFICE':
            if office.maskTime>120:
                blackscreen.opacity=255
                WF.pos='P&S'
                office.inside=False
    if office.maskTime>120:
        sfx.stare.stop()
        if blackscreen.opacity>=0:
            blackscreen.opacity-=5
        if blackscreen.opacity<=0:
            toybonnie.rect.x=WIDTH/1.3714
            toybonnie.dx=0
            toychica.rect.x=0
            toychica.dx=0
            office.maskTime=0
            
            
            
    office.rect.x+=office.dx
    drawMaskAnimation()
    drawCameraAnimation() 
    office.deskFrame+=1
    if office.deskFrame>4:
        office.deskFrame=0
        
    if office.maskFrame<9 and player.maskOn:
        office.maskFrame+=1
        office.light='NONE'
    elif office.maskFrame>=0 and player.maskOn==False:
        office.maskFrame-=1
    if office.maskFrame<0:
        office.maskFrames=0
        
    if monitor.frame<=11 and player.camsUp:
        monitor.frame+=1
    elif monitor.frame>=0 and player.camsUp==False:
        monitor.frame-=1
    if monitor.frame<0:
        monitor.frame=0
        
    if office.rect.right<WIDTH:
        office.rect.right=WIDTH
        office.side='NONE'
    elif office.rect.x>0:
        office.side='NONE'
        office.rect.x=0
def PlayAmbience():

    if player.maskOn==True and office.maskFrame==1:
        sfx.maskon.play()
        sfx.fansound.play(-1)
        sfx.ambience3.play(-1)
    if player.maskOn==True and office.maskFrame==8:
        sfx.maskbreaths.play(-1)
        
    if player.maskOn==False  and office.maskFrame==6:
        sfx.maskbreaths.stop()
        sfx.maskoff.play()
    if player.camsUp==True and monitor.frame==1:
        sfx.camBackground.play(-1)
        sfx.camup.play()
    if player.camsUp==False and monitor.frame==6:
        sfx.camBackground.stop()
        sfx.camdown.play()
    if player.camsUp:
        sfx.fansound.set_volume(.3)
        sfx.ambience3.set_volume(.3) 
    else:
        sfx.fansound.set_volume(1)
        sfx.ambience3.set_volume(1)
    
def syncMove(sprite):
    sprite.rect.x+=sprite.dx
    if office.side=='RIGHT': 
        sprite.dx=-25
    elif office.side=='LEFT':
        sprite.dx=25
    elif office.side=='NONE':
        sprite.dx=0
def drawOffice():
    #changes office state / sprite depending on which lights are on / animatronics in hall or vent 
    if office.light=='NONE':
        office.image=officeImages['ONN']
        screen.blit(leftOff.image, leftOff.rect)
        screen.blit(rightOff.image,rightOff.rect)
    elif office.light=='LEFT':
        sfx.buzzlight.play()
        if TC.pos!='OFFICE':
            office.image=officeImages['OLN']
        elif TC.pos=='OFFICE':
            office.image=officeImages['OL_T-CHICA2']
        screen.blit(leftOn.image, leftOn.rect)
        screen.blit(rightOff.image,rightOff.rect)
        player.flashbattery-=.05
    elif office.light=='RIGHT':
        sfx.buzzlight.play()
        if TB.pos!='OFFICE' and MA.pos!='OFFICE':
            office.image=officeImages['ORN']
        elif TB.pos=='OFFICE':
            office.image=officeImages['OR_T-BONNIE1']
        elif MA.pos=='OFFICE':
            office.image=officeImages['OR_MANGLE2']
        screen.blit(leftOff.image, leftOff.rect)
        screen.blit(rightOn.image,rightOn.rect)
        player.flashbattery-=.05
    elif office.light=='FRONT':
        sfx.buzzlight.play()
        WFO.value=0
        player.flashbattery-=.05
        if TC.pos!='OFFICE-HALLWAY' and TF.pos!='OFFICE-HALL1' and TF.pos!='OFFICE-HALL2' and WB.pos!='OFFICE-HALL' and WF.pos!='OFFICE-HALL' and MA.pos!='OFFICE-HALL' and WFO.pos!='OFFICE-HALL' and GF.pos!='OFFICE-HALL':
            office.image=officeImages['OFN']
        elif GF.pos=='OFFICE-HALL':
            office.image=officeImages['OF_G-FREDDY']
        elif WFO.pos=='OFFICE-HALL':
            office.image=officeImages['OF_W-FOXY1']
        elif WF.pos=='OFFICE-HALL':
            office.image=officeImages['OF_W-FREDDY1']
        elif TF.pos=='OFFICE-HALL2':
            office.image=officeImages['OF_T-FREDDY2']
        elif TF.pos=='OFFICE-HALL1':
            office.image=officeImages['OF_T-FREDDY1']
        elif TC.pos=='OFFICE-HALLWAY':
            office.image=officeImages['OF_T-CHICA1']
        elif WB.pos=='OFFICE-HALL':
            office.image=officeImages['OF_W-BONNIE1']
        elif MA.pos=='OFFICE-HALL':
            office.image=officeImages['OF_MANGLE1']
        screen.blit(leftOff.image, leftOff.rect)
        screen.blit(rightOff.image,rightOff.rect)
    if office.inside:
        if WB.pos=='IN-OFFICE':
            office.image=officeImages['ON_W-BONNIE2']
        elif WF.pos=='IN-OFFICE':
            office.image=officeImages['ON_W-FREDDY2']
        elif WC.pos=='IN-OFFICE':
            office.image=officeImages['ON_W-CHICA']
    
def drawFanAnimation():

#Desk Fan animation
    if office.deskFrame<=1:
        screen.blit(desk1.image,desk1.rect)
    elif office.deskFrame==2:
        screen.blit(desk2.image,desk2.rect)
    elif office.deskFrame==3:
        screen.blit(desk3.image,desk3.rect)
    elif office.deskFrame==4:
        screen.blit(desk4.image,desk4.rect)
def drawMaskAnimation():
    #mask animation
    if office.maskFrame==1:
        mask.image=officeIntImages['MASK-F1']
    elif office.maskFrame==2:
        mask.image=officeIntImages['MASK-F2']
    elif office.maskFrame==3:
        mask.image=officeIntImages['MASK-F3']
    elif office.maskFrame==4:
        mask.image=officeIntImages['MASK-F4']
    elif office.maskFrame==5:
        mask.image=officeIntImages['MASK-F5']
    elif office.maskFrame==6:
        mask.image=officeIntImages['MASK-F6']
    elif office.maskFrame==7:
        mask.image=officeIntImages['MASK-F7']
    elif office.maskFrame==8:
        mask.image=officeIntImages['MASK-F7']
    elif office.maskFrame==9:
        mask.image=officeIntImages['MASK-F9']
    
def drawStaticAnimation():
    
    if static.frame==1:
        static.image=overlayImages['STATIC1']
    elif static.frame==2:
        static.image=overlayImages['STATIC2']
    elif static.frame==3:
        static.image=overlayImages['STATIC3']
    elif static.frame==4:
        static.image=overlayImages['STATIC4']
    elif static.frame==5:
        static.image=overlayImages['STATIC5']
    elif static.frame==6:
        static.image=overlayImages['STATIC6']
def drawCameraAnimation():
    
    if monitor.frame==1:
        monitor.image=officeIntImages['CAM-F1']
    elif monitor.frame==2:
        monitor.image=officeIntImages['CAM-F2']
    elif monitor.frame==3:
        monitor.image=officeIntImages['CAM-F3']
    elif monitor.frame==4:
        monitor.image=officeIntImages['CAM-F4']
    elif monitor.frame==5:
        monitor.image=officeIntImages['CAM-F5']
    elif monitor.frame==6:
        monitor.image=officeIntImages['CAM-F6']
    elif monitor.frame==7:
        monitor.image=officeIntImages['CAM-F7']
    elif monitor.frame==8:
        monitor.image=officeIntImages['CAM-F8']
    elif monitor.frame==9:
        monitor.image=officeIntImages['CAM-F9']
    elif monitor.frame==10:
        monitor.image=officeIntImages['CAM-F10']
    elif monitor.frame==11:
        monitor.image=officeIntImages['CAM-F11']
        if player.camsUp:
            if player.currentCam=='PRISECOUNTER':
                sfx.musicbox.play()
        else:
            sfx.musicbox.stop()
def drawWhiteAnimation():
    
    if white.frame==1:
        white.image=overlayImages['WHITE1']
        sfx.blip.play()
        
    if white.frame==2:
        white.image=overlayImages['WHITE2']
    if white.frame==3:
        white.image=overlayImages['WHITE3']
    if white.frame==4:
        white.image=overlayImages['WHITE4']
    if white.frame==5:
        white.image=overlayImages['WHITE5']
def drawFlashlightBattery():
    if player.flashbattery>=80:
        flashlight.image=officeIntImages['FLASHLIGHT-1']
    elif player.flashbattery>=60:
        flashlight.image=officeIntImages['FLASHLIGHT-2']
    elif player.flashbattery>=40:
        flashlight.image=officeIntImages['FLASHLIGHT-3']
    elif player.flashbattery>=20:
        flashlight.image=officeIntImages['FLASHLIGHT-4']
    elif player.flashbattery<=0:
        flashlight.image=officeIntImages['FLASHLIGHT-5']
def ToyBonnieJS():
    if TB.attack:
        if TB.frame<13:
            TB.frame+=1
    if TB.frame==1:
        TB.image=animatronicImages['ANIM-TB_JS1']
        sfx.js1.play()
    if TB.frame==2:
        TB.image=animatronicImages['ANIM-TB_JS2']
    if TB.frame==3:
        TB.image=animatronicImages['ANIM-TB_JS3']
    if TB.frame==4:
        TB.image=animatronicImages['ANIM-TB_JS4']
    if TB.frame==5:
        TB.image=animatronicImages['ANIM-TB_JS5']
    if TB.frame==6:
        TB.image=animatronicImages['ANIM-TB_JS6']
    if TB.frame==7:
        TB.image=animatronicImages['ANIM-TB_JS7']
    if TB.frame==8:
        TB.imame=animatronicImages['ANIM-TB_JS8']
    if TB.frame==9:
        TB.image=animatronicImages['ANIM-TB_JS9']
    if TB.frame==10:
        TB.image=animatronicImages['ANIM-TB_JS10']
    if TB.frame==11:
        TB.image=animatronicImages['ANIM-TB_JS11']
    if TB.frame==12:
        TB.image=animatronicImages['ANIM-TB_JS12']
    if TB.frame==13:
        TB.image=animatronicImages['ANIM-TB_JS13']
def updateCams():
    
    if cam.staticTimer>0:
        cam.staticTimer-=1
    if cam.staticTimer<=0:
        cam.staticTimer=0
    
    if monitor.frame>9 and GF.seen:
        GF.pos='N/A'
        GF.seen=False
        
    cam.moveTimer+=1
    static.frame+=1
    
    if P.out:
        cam.puppetMoveTimer+=1
    if static.frame>6:
        static.frame=0
    drawStaticAnimation()
    drawWhiteAnimation()
    
    if white.ani:
        white.image.set_alpha(255)
        white.frame+=1
        if white.frame>=5:
            white.frame=0
            white.ani=False
    else:
        white.image.set_alpha(0)
    static.image.set_alpha(random.randint(60,140))
    
    if cam.move=='RIGHT':
        cam.rect.x+=cam.dx
        manglePC.rect.x+=cam.dx
        mangleGA.rect.x+=cam.dx
        mangleMH.rect.x+=cam.dx
        mangleP2.rect.x+=cam.dx
    elif cam.move=='LEFT':
        cam.rect.x-=cam.dx
        manglePC.rect.x-=cam.dx
        mangleGA.rect.x-=cam.dx
        mangleMH.rect.x-=cam.dx
        mangleP2.rect.x-=cam.dx
    if(cam.rect.left>=0 or cam.rect.right<=WIDTH):
        if cam.move=='LEFT':
            cam.move='RIGHT'
        elif cam.move=='RIGHT':
            cam.move='LEFT'
def camstatic():
    
    if cam.staticTimer>0:
        cam.image=camImages['P&S-FULL/N']
        sfx.popstatic.play()
    else:
        sfx.popstatic.stop()
def drawCams():

    if player.currentCam=='SHOWSTAGE':
        if TB.pos=='SHOWSTAGE' and TC.pos=='SHOWSTAGE' and TF.pos=='SHOWSTAGE':
            cam.image=camImages['SHOWSTAGE-FULL/N']
            if cam.flash:
                cam.image=camImages['SHOWSTAGE-FULL/L']
        elif TB.pos!='SHOWSTAGE' and TC.pos=='SHOWSTAGE' and TF.pos=='SHOWSTAGE':
            cam.image=camImages['SHOWSTAGE-F&C/N']
            if cam.flash:
                cam.image=camImages['SHOWSTAGE-F&C/L']
        elif TB.pos!='SHOWSTAGE' and TC.pos!='SHOWSTAGE' and TF.pos=='SHOWSTAGE':
            cam.image=camImages['SHOWSTAGE-F/N']
            if cam.flash:
                cam.image=camImages['SHOWSTAGE-F/L']
        elif TB.pos!='SHOWSTAGE' and TC.pos!='SHOWSTAGE' and TF.pos!='SHOWSTAGE':
            cam.image=camImages['SHOWSTAGE-EMPTY']
            if cam.flash:
                cam.image=camImages['SHOWSTAGE-EMPTY']
        if TB.pos=='PARTYROOM3' or TC.pos=='MAINHALL' or TF.pos=='GAMEAREA':
            camstatic()
        textCam.image=camUIImages['TEXT-SHOWSTAGE']
        camGbox.rect.x=cambox9.rect.x
        camGbox.rect.y=cambox9.rect.y
            
    elif player.currentCam=='GAMEAREA':
        if BB.pos=='GAMEAREA':
            cam.image=camImages['GAMEAREA-BB/N']
            if cam.flash:
                if TF.pos!='GAMEAREA' and BB.pos=='GAMEAREA':
                    cam.image=camImages['GAMEAREA-BB/L']
                elif TF.pos=='GAMEAREA' and BB.pos=='GAMEAREA':
                    cam.image=camImages['GAMEAREA-BB&F/L']
        else:
            cam.image=camImages['GAMEAREA-EMPTY/N']
            if cam.flash:
                if TF.pos=='GAMEAREA' and BB.pos!='GAMEAREA':
                    cam.image=camImages['GAMEAREA-F/L']
                elif TF.pos!='GAMEAREA' and BB.pos!='GAMEAREA':
                    cam.image=camImages['GAMEAREA-EMPTY/L']
        textCam.image=camUIImages['TEXT-GAMEAREA']
        camGbox.rect.x=cambox10.rect.x
        camGbox.rect.y=cambox10.rect.y
        if BB.pos=='N/A-1' or TF.pos=='GAMEAREA' or TF.pos=='OFFICE-HALL1' or MA.pos=='GAMEAREA' or MA.pos=='MAINHALL':
            camstatic()
        
    elif player.currentCam=='PRISECOUNTER':
        cam.image=camImages['PRISECOUNTER-EMPTY/N']
        textCam.image=camUIImages['TEXT-PRISECOUNTER']
        camGbox.rect.x=cambox11.rect.x
        camGbox.rect.y=cambox11.rect.y
        if cam.flash:
            if P.pos=='PRISECOUNTER':
                cam.image=camImages['PRISECOUNTER-M1/L']
            elif P.pos=='PRISECOUNTER-1':
                cam.image=camImages['PRISECOUNTER-M2/L']
            elif P.pos=='PRISECOUNTER-2':
                cam.image=camImages['PRISECOUNTER-M3/L']
            else:
                cam.image=camImages['PRISECOUNTER-EMPTY/L']
        if MA.pos=='PRISECOUNTER' or MA.pos=='GAMEAREA':
            camstatic()
            
    elif player.currentCam=='KIDSCOVE':
        cam.image=camImages['KIDSCOVE-EMPTY/N']
        textCam.image=camUIImages['TEXT-KIDSCOVE']
        camGbox.rect.x=cambox12.rect.x
        camGbox.rect.y=cambox12.rect.y
        if cam.flash:
            if MA.pos=='KIDSCOVE':
                cam.image=camImages['KIDSCOVE-M/L']
            else:
                cam.image=camImages['KIDSCOVE-EMPTY/L']
        if MA.pos=='PRISECOUNTER':
            camstatic()
    elif player.currentCam=='MAINHALL':
        if TC.pos!='MAINHALL':
            cam.image=camImages['MAINHALL-EMPTY/N']
            if cam.flash:
                if WB.pos!='MAINHALL' and WF.pos!='MAINHALL':
                    cam.image=camImages['MAINHALL-EMPTY/L']
                elif WF.pos=='MAINHALL':
                    cam.image=camImages['MAINHALL-WF/L']
                elif WB.pos=='MAINHALL':
                    cam.image=camImages['MAINHALL-WB/L']
        elif TC.pos=='MAINHALL':
            cam.image=camImages['MAINHALL-TC/N']
            if cam.flash:
                cam.image=camImages['MAINHALL-TC/L']
        if TC.pos=='MAINHALL' or TC.pos=='PARTYROOM4' or WF.pos=='MAINHALL' or WF.pos=='PARTYROOM3' or WB.pos=='MAINHALL' or WB.pos=='OFFICE-HALL' or MA.pos=='MAINHALL' or MA.pos=='OFFICE-HALL':
            camstatic()
        textCam.image=camUIImages['TEXT-MAINHALL']
        camGbox.rect.x=cambox7.rect.x
        camGbox.rect.y=cambox7.rect.y
        
    elif player.currentCam=='P&S':
        cam.image=camImages['P&S-FULL/N']
        textCam.image=camUIImages['TEXT-P&S']
        camGbox.rect.x=cambox8.rect.x
        camGbox.rect.y=cambox8.rect.y
        if cam.flash:
            if WF.pos=='P&S' and WB.pos=='P&S' and WC.pos=='P&S':
                cam.image=camImages['P&S-FULL/L']
            elif WF.pos=='P&S' and WB.pos!='P&S' and WC.pos=='P&S':
                cam.image=camImages['P&S-WF&WC/L']
            elif WF.pos=='P&S' and WB.pos!='P&S' and WC.pos!='P&S':
                cam.image=camImages['P&S-WF/L']
            elif WF.pos!='P&S' and WB.pos!='P&S' and WC.pos!='P&S':
                cam.image=camImages['P&S-EMPTY/L']
        if WF.pos=='MAINHALL' or WB.pos=='MAINHALL' or WC.pos=='PARTYROOM4':
            camstatic()
    elif player.currentCam=='PARTYROOM1':
        cam.image=camImages['PARTYROOM1-EMPTY/N']
        textCam.image=camUIImages['TEXT-PARTYROOM1']
        camGbox.rect.x=cambox1.rect.x
        camGbox.rect.y=cambox1.rect.y
        if cam.flash:
            if TC.pos!='PARTYROOM1' and WB.pos!='PARTYROOM1'and WF.pos!='PARTYROOM1':
                cam.image=camImages['PARTYROOM1-EMPTY/L']
            elif TC.pos=='PARTYROOM1':
                cam.image=camImages['PARTYROOM1-TC/L']
            elif WB.pos=='PARTYROOM1':
                cam.image=camImages['PARTYROOM1-WB/L']
        if TC.pos=='PARTYROOM1' or TC.pos=='LEFTVENT' or WB.pos=='PARTYROOM1' or WB.pos=='LEFTVENT':
            camstatic()
            
    elif player.currentCam=='PARTYROOM2':
        if WC.pos!='PARTYROOM2':
            cam.image=camImages['PARTYROOM2-EMPTY/N']
            if cam.flash:
                if TB.pos!='PARTYROOM2' and WC.pos!='PARTYROOM2':
                    cam.image=camImages['PARTYROOM2-EMPTY/L']
                elif TB.pos=='PARTYROOM2':
                    cam.image=camImages['PARTYROOM2-TB/L']
        elif WC.pos=='PARTYROOM2':
            cam.image=camImages['PARTYROOM2-WC/N']
            if cam.flash:
                cam.image=camImages['PARTYROOM2-WC/L']
        if TB.pos=='PARTYROOM2' or TB.pos=='RIGHTVENT' or WC.pos=='PARTYROOM2' or WC.pos=='RIGHTVENT':
            camstatic()
        textCam.image=camUIImages['TEXT-PARTYROOM2']
        camGbox.rect.x=cambox2.rect.x
        camGbox.rect.y=cambox2.rect.y
        
            
    elif player.currentCam=='PARTYROOM3':
        if WF.pos!='PARTYROOM3':
            cam.image=camImages['PARTYROOM3-EMPTY/N']
            if cam.flash:
                if TB.pos!='PARTYROOM3':
                    cam.image=camImages['PARTYROOM3-EMPTY/L']
                else:
                    cam.image=camImages['PARTYROOM3-TB/L']
        elif WF.pos=='PARTYROOM3':
            cam.image=camImages['PARTYROOM3-WF/N']
            if cam.flash:
                cam.image=camImages['PARTYROOM3-WF/L']
        if TB.pos=='PARTYROOM3' or TB.pos=='PARTYROOM4' or WF.pos=='PARTYROOM3' or WF.pos=='OFFICE-HALL':
            camstatic()
        textCam.image=camUIImages['TEXT-PARTYROOM3']
        camGbox.rect.x=cambox3.rect.x
        camGbox.rect.y=cambox3.rect.y
        
            
    elif player.currentCam=='PARTYROOM4':
        if TB.pos!='PARTYROOM4':
            cam.image=camImages['PARTYROOM4-EMPTY/N']
            if cam.flash:
                if TC.pos!='PARTYROOM4' and WC.pos!='PARTYROOM4':
                    cam.image=camImages['PARTYROOM4-EMPTY/L']
                elif TC.pos=='PARTYROOM4':
                    cam.image=camImages['PARTYROOM4-TC/L']
                elif WC.pos=='PARTYROOM4':
                    cam.image=camImages['PARTYROOM4-WC/L']
        elif TB.pos=='PARTYROOM4':
            cam.image=camImages['PARTYROOM4-TB/N']
            if cam.flash:
                cam.image=camImages['PARTYROOM4-TB/L']
        if TB.pos=='PARTYROOM4' or TB.pos=='PARTYROOM2' or WC.pos=='PARTYROOM4' or WC.pos=='PARTYROOM2':
            camstatic()
        textCam.image=camUIImages['TEXT-PARTYROOM4']
        camGbox.rect.x=cambox4.rect.x
        camGbox.rect.y=cambox4.rect.y
        
    elif player.currentCam=='LEFTVENT':
        cam.image=camImages['LEFTVENT-EMPTY/N']
        textCam.image=camUIImages['TEXT-LEFTAIRVENT']
        camGbox.rect.x=cambox5.rect.x
        camGbox.rect.y=cambox5.rect.y
        if cam.flash:
            if TC.pos!='LEFTVENT' and WB.pos!='LEFTVENT':
                cam.image=camImages['LEFTVENT-EMPTY/L']
            elif TC.pos=='LEFTVENT':
                cam.image=camImages['LEFTVENT-TC/L']
            elif WB.pos=='LEFTVENT':
                cam.image=camImages['LEFTVENT-WB/L']
            elif BB.pos=='LEFTVENT':
                cam.image=camImages['LEFTVENT-BB/L']
        if TC.pos=='LEFTVENT' or TC.pos=='OFFICE' or WB.pos=='LEFTVENT' or WB.pos=='OFFICE' or BB.pos=='LEFTVENT' or BB.pos=='OFFICE':
            camstatic()
    elif player.currentCam=='RIGHTVENT':
        cam.image=camImages['RIGHTVENT-EMPTY/N']
        textCam.image=camUIImages['TEXT-RIGHTAIRVENT']
        camGbox.rect.x=cambox6.rect.x
        camGbox.rect.y=cambox6.rect.y
        if cam.flash:
            if TB.pos!='RIGHTVENT' and WC.pos!='RIGHTVENT':
                cam.image=camImages['RIGHTVENT-EMPTY/L']
            elif TB.pos=='RIGHTVENT':
                cam.image=camImages['RIGHTVENT-TB/L']
            elif WC.pos=='RIGHTVENT':
                cam.image=camImages['RIGHTVENT-WC/L']
            elif MA.pos=='RIGHTVENT':
                cam.image=camImages['RIGHTVENT-M/L']
        if TB.pos=='RIGHTVENT' or TB.pos=='OFFICE' or WC.pos=='RIGHTVENT' or WC.pos=='IN-OFFICE' or MA.pos=='RIGHTVENT' or MA.pos=='OFFICE':
            camstatic()
def drawMusicBox():
    if P.timer>=2000:
        musicBox.image=camUIImages['CAM-MUSIC_BAR21']
    elif P.timer>=1900:
        musicBox.image=camUIImages['CAM-MUSIC_BAR20']
    elif P.timer>=1800:
        musicBox.image=camUIImages['CAM-MUSIC_BAR19']
    elif P.timer>=1700:
        musicBox.image=camUIImages['CAM-MUSIC_BAR18']
    elif P.timer>=1600:
        musicBox.image=camUIImages['CAM-MUSIC_BAR17']
    elif P.timer>=1500:
        musicBox.image=camUIImages['CAM-MUSIC_BAR16']
    elif P.timer>=1400:
        musicBox.image=camUIImages['CAM-MUSIC_BAR15']
    elif P.timer>=1300:
        musicBox.image=camUIImages['CAM-MUSIC_BAR14']
    elif P.timer>=1200:
        musicBox.image=camUIImages['CAM-MUSIC_BAR13']
    elif P.timer>=1100:
        musicBox.image=camUIImages['CAM-MUSIC_BAR12']
    elif P.timer>=1000:
        musicBox.image=camUIImages['CAM-MUSIC_BAR11']
    elif P.timer>=900:
        musicBox.image=camUIImages['CAM-MUSIC_BAR10']
    elif P.timer>=800:
        musicBox.image=camUIImages['CAM-MUSIC_BAR9']
    elif P.timer>=700:
        musicBox.image=camUIImages['CAM-MUSIC_BAR8']
    elif P.timer>=600:
        musicBox.image=camUIImages['CAM-MUSIC_BAR7']
    elif P.timer>=500:
        musicBox.image=camUIImages['CAM-MUSIC_BAR6']
    elif P.timer>=400:
        musicBox.image=camUIImages['CAM-MUSIC_BAR5']
    elif P.timer>=300:
        musicBox.image=camUIImages['CAM-MUSIC_BAR4']
    elif P.timer>=200:
        musicBox.image=camUIImages['CAM-MUSIC_BAR2']
    elif P.timer>=100:
        musicBox.image=camUIImages['CAM-MUSIC_BAR1']
def draw():
    screen.fill(BGCOLOR)
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    screen.blit(office.image,office.rect)
    if player.camsUp==False:
        drawOffice()
    if TF.pos=='IN-OFFICE':
        screen.blit(toyfreddy.image,toyfreddy.rect)
    if GF.pos=='IN-OFFICE':
        screen.blit(goldenfreddy.image,goldenfreddy.rect)
    drawFanAnimation()
#draws UI
    drawFlashlightBattery()
    if MA.pos=='IN-OFFICE':
        screen.blit(mangleO.image,mangleO.rect)
    screen.blit(maskButton.image,maskButton.rect)
    screen.blit(monitor.image,monitor.rect)
    
    if office.inside==True and TB.pos=='IN-OFFICE' and office.maskFrame>=6:
        screen.blit(toybonnie.image,toybonnie.rect)
    elif office.inside==True and TC.pos=='IN-OFFICE'  and office.maskFrame>=6:
        screen.blit(toychica.image,toychica.rect)
    if player.camsUp == True and monitor.frame>=11:
        drawCams()
        screen.blit(cam.image,cam.rect)
        if MA.pos=='GAMEAREA' and player.currentCam=='GAMEAREA':
            screen.blit(mangleGA.image,mangleGA.rect)
        elif MA.pos=='PRISECOUNTER' and player.currentCam=='PRISECOUNTER':
            screen.blit(manglePC.image,manglePC.rect)
        elif MA.pos=='MAINHALL' and player.currentCam=='MAINHALL':
            screen.blit(mangleMH.image,mangleMH.rect)
        if MA.pos=='PARTYROOM2' and player.currentCam=='PARTYROOM2':
            screen.blit(mangleP2.image,mangleP2.rect)
        screen.blit(static.image,static.rect)
        screen.blit(camMap.image,camMap.rect)
        screen.blit(cambox1.image,cambox1.rect)
        screen.blit(cambox2.image,cambox2.rect)
        screen.blit(cambox3.image,cambox3.rect)
        screen.blit(cambox4.image,cambox4.rect)
        screen.blit(cambox5.image,cambox5.rect)
        screen.blit(cambox6.image,cambox6.rect)
        screen.blit(cambox7.image,cambox7.rect)
        screen.blit(cambox8.image,cambox8.rect)
        screen.blit(cambox9.image,cambox9.rect)
        screen.blit(cambox10.image,cambox10.rect)
        screen.blit(cambox11.image,cambox11.rect)
        screen.blit(cambox12.image,cambox12.rect)
        screen.blit(camGbox.image,camGbox.rect)
        screen.blit(Text01.image,Text01.rect)
        screen.blit(Text02.image,Text02.rect)
        screen.blit(Text03.image,Text03.rect)
        screen.blit(Text04.image,Text04.rect)
        screen.blit(Text05.image,Text05.rect)
        screen.blit(Text06.image,Text06.rect)
        screen.blit(Text07.image,Text07.rect)
        screen.blit(Text08.image,Text08.rect)
        screen.blit(Text09.image,Text09.rect)
        screen.blit(Text10.image,Text10.rect)
        screen.blit(Text11.image,Text11.rect)
        screen.blit(Text12.image,Text12.rect)
        screen.blit(textCam.image,textCam.rect)
        if player.currentCam=='PRISECOUNTER':
            drawMusicBox()
            if P.recharge==False:
                screen.blit(musicButtonOff.image,musicButtonOff.rect)
            else:
                screen.blit(musicButtonOn.image,musicButtonOn.rect)
            screen.blit(textWindUp.image,textWindUp.rect)
            screen.blit(textClick.image,textClick.rect)
            if P.timer>0:
                screen.blit(musicBox.image,musicBox.rect)
        screen.blit(camDot.image,camDot.rect)
        screen.blit(camOutline.image,camOutline.rect)
    screen.blit(camButton.image,camButton.rect)
    screen.blit(amText.image,amText.rect)
    screen.blit(nightText.image,nightText.rect)
    screen.blit(flashlight.image,flashlight.rect)
    screen.blit(flashlightText.image,flashlightText.rect)
    if TB.attack:
        screen.blit(TB.image,TB.rect)
    screen.blit(white.image,white.rect)
    screen.blit(blackscreen.image,blackscreen.rect)
    screen.blit(mask.image,mask.rect)
    pygame.display.update()
    

def onMousePress(x, y):
    #Charges music Box
    
    if player.currentCam=='PRISECOUNTER' and player.camsUp==True and x>WIDTH/3.2 and x<WIDTH/3.2 + WIDTH/7.111 and y>HEIGHT/1.384 and y<HEIGHT/1.384 +HEIGHT/9.818:
        P.recharge=True
        sfx.windup.play(-1)
    else:
        P.recharge=False
        sfx.windup.stop()
    
    
    #Turns office lights on depending on where you click
    if player.maskOn==False:
        if x <= WIDTH/4.8 and y >=HEIGHT/2.7 and y<=HEIGHT/1.08:
            office.light='LEFT'
        elif x >=WIDTH/1.263 and y >=HEIGHT/2.7 and y<=HEIGHT/1.08:
            office.light='RIGHT'
        elif x>=WIDTH/2.953 and x<=WIDTH/1.476:
            office.light='FRONT'
            WFO.attackTimer=50
            if GF.pos=='OFFICE-HALL':
                GF.increase=True
    #changes current camera selected when cams up
    if player.camsUp:       
        if x>=WIDTH/1.745 and x<=WIDTH/1.597 and y>=HEIGHT/1.469 and y<=HEIGHT/1.344:
            player.currentCam='PARTYROOM1'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.432 and x<=WIDTH/1.3314 and y>=HEIGHT/1.469 and y<=HEIGHT/1.344:
            player.currentCam='PARTYROOM2'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.745 and x<=WIDTH/1.59 and y>=HEIGHT/1.741 and y<=HEIGHT/1.569:
            player.currentCam='PARTYROOM3'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.432 and x<=WIDTH/1.331 and y>=HEIGHT/1.741 and y<=HEIGHT/1.569:
            player.currentCam='PARTYROOM4'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.729 and x<=WIDTH/1.584 and y>=HEIGHT/1.22 and y<=HEIGHT/1.133:
            player.currentCam='LEFTVENT'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.44 and x<=WIDTH/1.34 and y>=HEIGHT/1.22 and y<=HEIGHT/1.133:
            player.currentCam='RIGHTVENT'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.39 and x<=WIDTH/1.295 and y>=HEIGHT/2.076 and y<=HEIGHT/1.836:
            player.currentCam='MAINHALL'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.745 and x<=WIDTH/1.59 and y>=HEIGHT/2.16 and y<=HEIGHT/1.901:
            player.currentCam='P&S'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.136 and x<=WIDTH/1.07 and y>=HEIGHT/2.37 and y<=HEIGHT/2.065:
            player.currentCam='SHOWSTAGE'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.24 and x<=WIDTH/1.169 and y>=HEIGHT/1.648 and y<=HEIGHT/1.493:
            player.currentCam='GAMEAREA'
            white.ani=True
            sfx.musicbox.stop()
            sfx.popstatic.stop()
        elif x>=WIDTH/1.09 and x<=WIDTH/1.036 and y>=HEIGHT/1.928 and y<=HEIGHT/1.719:
            player.currentCam='PRISECOUNTER'
            sfx.musicbox.play(-1)
            sfx.popstatic.stop()
            white.ani=True
        elif x>=WIDTH/1.122 and x<=WIDTH/1.059 and y>=HEIGHT/1.449 and y<=HEIGHT/1.328:
            player.currentCam='KIDSCOVE'
            sfx.musicbox.stop()
            sfx.popstatic.stop()
            white.ani=True
def onMouseRelease(x, y):
    if player.maskOn==False:
        office.light='NONE'
        sfx.buzzlight.stop()
        GF.increase=False
    if player.currentCam=='PRISECOUNTER' and player.camsUp==True and x>WIDTH/3.2 and x<WIDTH/3.2 + WIDTH/7.111 and y>HEIGHT/1.384 and y<HEIGHT/1.384 +HEIGHT/9.818:
        P.recharge=False
        sfx.windup.stop()
    

def onMouseMove(x, y):
    if x >=WIDTH/1.573 and office.rect.right>WIDTH:
        office.dx=-25
        office.side='RIGHT'
    elif x<=WIDTH/2.66 and office.rect.left<0:
        office.dx=25
        office.side='LEFT'
    else:
        office.dx=0
        office.side='NONE'
        
        #For use of the mask button
    if player.camsUp==False:
        if (x >=WIDTH/192 and x<WIDTH/1.939 and y>=HEIGHT/1.186 and y<=HEIGHT/1.048)==False:
            if player.maskOn==False:
                player.C=0
            elif player.maskOn==True:
                player.C=2
            
        if x >=WIDTH/38.4 and x<WIDTH/2.02 and y>=HEIGHT/1.136 and y<=HEIGHT/1.09090909:
            if player.C==0:
                player.maskOn=True
            elif player.C==2:
                player.maskOn=False
       
                
        #For use of the cam button
    if player.maskOn==False:
        if (x >=WIDTH/1.979 and x<WIDTH/1.026 and y>=HEIGHT/1.186 and y<=HEIGHT/1.048)==False:
            if player.camsUp==False:
                player.C2=0
            elif player.camsUp==True:
                player.C2=2
            
        if x >=WIDTH/1.900 and x<WIDTH/1.00523 and y>=HEIGHT/1.136 and y<=HEIGHT/1.09090909:
            if player.C2==0:
                player.camsUp=True
            elif player.C2==2:
                player.camsUp=False
                sfx.popstatic.stop()
    if (player.currentCam=='PRISECOUNTER' and player.camsUp==True and x>WIDTH/3.2 and x<WIDTH/3.2 + WIDTH/7.111 and y>HEIGHT/1.384 and y<HEIGHT/1.384 +HEIGHT/9.818)==False:
        P.recharge=False
        sfx.windup.stop()

def onKeyPress(key):
    pass
    
    if office.light=='NONE' and key == pygame.K_SPACE and player.maskOn==False:
        office.light='FRONT'
    if key == pygame.K_SPACE:
        cam.flash=True
        player.flashbattery-=.02

def onKeyRelease(key):
    if key == pygame.K_SPACE and player.maskOn==False:
        office.light='NONE'
        sfx.buzzlight.stop()
    if key == pygame.K_SPACE:
        cam.flash=False
    
def updateAi():
    if(cam.moveTimer>=150):
        ToyBonnieAi()
        ToyChicaAi()
        ToyFreddyAi()
        WitheredBonnieAi()
        WitheredChicaAi()
        WitheredFreddyAi()
        WitheredFoxyAi()
        BalloonBoyAi()
        MangleAi()
        GoldenFreddyOfficeAi()
        cam.moveTimer=0
    if cam.puppetMoveTimer>=30 and P.out:
        PuppetAi()
        cam.puppetMoveTimer=0
    if GF.timer>=30:
        GoldenFreddyHallAi()
        GF.timer=0
def ToyBonnieAi():
    
    mChance=random.randint(1,20)
    if(TB.ai>=mChance):
        TB.move=True
        cam.staticTimer=random.randint(60,120)
    else:
        TB.move=False
    if TB.move:
        if TB.pos=='SHOWSTAGE':
            TB.pos='PARTYROOM3'
            TB.move=False
        elif TB.pos=='PARTYROOM3':
            TB.pos='PARTYROOM4'
            TB.move=False
        elif TB.pos=='PARTYROOM4':
            TB.pos='PARTYROOM2'
            TB.move=False
        elif TB.pos=='PARTYROOM2':
            TB.pos='RIGHTVENT'
            TB.move=False
        elif TB.pos=='RIGHTVENT':
            TB.pos='OFFICE'
            sfx.ventwalk.play()
            TB.move=False
        elif TB.pos=='OFFICE' and office.maskTime==0:
            TB.pos='IN-OFFICE'
            if player.maskOn==False or player.camsUp==True:
                TB.attack=True
                player.dead=True
                TB.move=False
            else:
                office.inside=True
                sfx.stare.play()
                TB.move=False
def ToyChicaAi():
    
    mChance=random.randint(1,20)
    if(TC.ai>=mChance):
        TC.move=True
        cam.staticTimer=random.randint(60,120)
    else:
        TC.move=False
        
    if TC.move:
        if TC.pos=='SHOWSTAGE' and TB.pos!='SHOWSTAGE':
            TC.pos='MAINHALL'
            TC.move=False
        elif TC.pos=='MAINHALL':
            TC.pos='PARTYROOM4'
            TC.move=False
        elif TC.pos=='PARTYROOM4':
            if office.hallfull==False:
                sfx.ambiencescary.play(-1)
            TC.pos='OFFICE-HALLWAY'
            TC.move=False
        elif TC.pos=='OFFICE-HALLWAY':
            TC.pos='PARTYROOM1'
            TC.move=False    
        elif TC.pos=='PARTYROOM1':
            TC.pos='LEFTVENT'
            TC.move=False
        elif TC.pos=='LEFTVENT':
            sfx.ventwalk.play()
            TC.pos='OFFICE'
            TC.move=False
        elif TC.pos=='OFFICE' and office.maskTime==0:
            TC.pos='IN-OFFICE'
            sfx.stare.play()
            office.inside=True
            TC.move=False
def ToyFreddyAi():
    
    mChance=random.randint(1,20)
    if(TF.ai>=mChance):
        TF.move=True
        cam.staticTimer=random.randint(60,120)
    else:
        TF.move=False
        
    if TF.move:
        if TF.pos=='SHOWSTAGE' and TC.pos!='SHOWSTAGE' and TB.pos!='SHOWSTAGE':
            TF.pos='GAMEAREA'
            TF.move=False
        elif TF.pos=='GAMEAREA':
            if office.hallfull==False:
                sfx.ambiencescary.play(-1)
            TF.pos='OFFICE-HALL1'
            TF.move=False
        elif TF.pos=='OFFICE-HALL1':
            TF.pos='OFFICE-HALL2'
            TF.move=False
        elif TF.pos=='OFFICE-HALL2' and player.camsUp==True and office.maskTime==0:
            TF.pos='IN-OFFICE'
            TF.move=False
            sfx.stare.play()
            office.inside=True
def WitheredBonnieAi():
    
    mChance=random.randint(1,20)
    if(WB.ai>=mChance):
        WB.move=True
        cam.staticTimer=random.randint(60,120)
    else:
        WB.move=False
        
    if WB.move:
        if WB.pos=='P&S':
            WB.pos='MAINHALL'
            WB.move=False
        elif WB.pos=='MAINHALL':
            if office.hallfull==False:
                sfx.ambiencescary.play(-1)
            WB.pos='OFFICE-HALL'
            WB.move=False
        elif WB.pos=='OFFICE-HALL':
            WB.pos='PARTYROOM1'
            WB.move=False
        elif WB.pos=='PARTYROOM1':
            sfx.ventwalk.play()
            WB.pos='LEFTVENT'
            WB.move=False
        elif WB.pos=='LEFTVENT'and office.maskTime==0:
            WB.pos='IN-OFFICE'
            WB.move=False
            sfx.stare.play()
            office.inside=True
def WitheredChicaAi():
    
    mChance=random.randint(1,20)
    if(WC.ai>=mChance):
        WC.move=True
        cam.staticTimer=random.randint(60,120)
    else:
        WC.move=False
        
    if WC.move:
        if WC.pos=='P&S' and WB.pos!='P&S':
            WC.pos='PARTYROOM4'
            WC.move=False
        elif WC.pos=='PARTYROOM4':
            WC.pos='PARTYROOM2'
            WC.move=False
        elif WC.pos=='PARTYROOM2':
            sfx.ventwalk.play()
            WC.pos='RIGHTVENT'
            WC.move=False
        elif WC.pos=='RIGHTVENT'and office.maskTime==0:
            WC.pos='IN-OFFICE'
            office.inside=True
            sfx.stare.play()
            WC.move=False
def WitheredFreddyAi():
    
    mChance=random.randint(1,20)
    if(WF.ai>=mChance):
        WF.move=True
        cam.staticTimer=random.randint(60,120)
    else:
        WF.move=False
        
    if WF.move:
        if WF.pos=='P&S' and WB.pos!='P&S' and WC.pos!='P&S':
            WF.pos='MAINHALL'
            WF.move=False
        elif WF.pos=='MAINHALL':
            WF.pos='PARTYROOM3'
            WF.move=False
        elif WF.pos=='PARTYROOM3':
            if office.hallfull==False:
                sfx.ambiencescary.play(-1)
            WF.pos='OFFICE-HALL'
            WF.move=False
        elif WF.pos=='OFFICE-HALL' and office.maskTime==0:
            WF.pos='IN-OFFICE'
            office.inside=True
            sfx.stare.play()
            WF.move=False
def WitheredFoxyAi():
    mChance= 21+random.randint(1,5) - WFO.value
    if(WFO.ai>=mChance):
        WFO.move=True
        
    else:
        WFO.move=False
        
    if WFO.move:
        if WFO.pos=='P&S':
            if office.hallfull==False:
                sfx.ambiencescary.play(-1)
            WFO.pos='OFFICE-HALL'
            WFO.attackTimer=50
            WFO.move=False
        elif WFO.pos=='OFFICE-HALL':
            if WFO.attackTimer>0:
                WFO.pos='P&S'
                WFO.move=False
            else:
                WFO.move=False
def WitheredFoxyAttack():
    if WFO.pos=='OFFICE-HALL':
        WFO.attackTimer-=1
        
def BalloonBoyAi():
    
    mChance=random.randint(1,20)
    if(BB.ai>=mChance):
        BB.move=True
        cam.staticTimer=random.randint(60,120)
    else:
        BB.move=False
        
    if BB.move:
        if BB.pos=='GAMEAREA':
            BB.pos='N/A-1'
            BB.move=False
        elif BB.pos=='N/A-1':
            BB.pos='N/A-2'
            BB.move=False
        elif BB.pos=='N/A-2':
            BB.pos='N/A-3'
            BB.move=False
        elif BB.pos=='N/A-3':
            BB.pos='LEFTVENT'
            BB.move=False
        elif BB.pos=='LEFTVENT':
            sfx.ventwalk.play()
            BB.pos='OFFICE'
            BB.move=False
        elif BB.pos=='OFFICE' and office.maskTime==0:
            BB.pos='IN-OFFICE'
            BB.move=False
def MangleAi():
    
    mChance=random.randint(1,20)
    if(MA.ai>=mChance):
        MA.move=True
        cam.staticTimer=random.randint(60,120)
    else:
        MA.move=False
        
    if MA.move:
        if MA.pos=='KIDSCOVE':
            MA.pos='PRISECOUNTER'
            MA.move=False
        elif MA.pos=='PRISECOUNTER':
            MA.pos='GAMEAREA'
            MA.move=False
        elif MA.pos=='GAMEAREA':
            MA.pos='MAINHALL'
            MA.move=False
        elif MA.pos=='MAINHALL':
            if office.hallfull==False:
                sfx.ambiencescary.play(-1)
            MA.pos='OFFICE-HALL'
            MA.move=False    
        elif MA.pos=='OFFICE-HALL':
            MA.pos='PARTYROOM2'
            MA.move=False
        elif MA.pos=='PARTYROOM2':
            MA.pos='RIGHTVENT'
            MA.move=False
        elif MA.pos=='RIGHTVENT':
            sfx.ventwalk.play()
            MA.pos='OFFICE'
            MA.move=False
        elif MA.pos=='OFFICE' and office.maskTime==0:
            MA.pos='IN-OFFICE'
            MA.move=False
def Musicbox():
    P.timertimer+=1
    if P.timer>=0 and P.timertimer>=2:
        if P.recharge==False:
            P.timer-=P.subtraction
        elif P.recharge and P.timer<2000:
            P.timer+=20
        P.timertimer=0
    
    if P.timer<0:
        P.timer=0
        P.out=True
    if P.timer>2000:
        P.timer=2000
def PuppetAi():
    mChance=random.randint(1,20)
    if(P.ai>=mChance):
        P.move=True
    else:
        P.move=False
    if P.move:
        if P.pos=='PRISECOUNTER':
            P.pos='PRISECOUNTER-1'
            P.move=False
        elif P.pos=='PRISECOUNTER-1':
            P.pos='PRISECOUNTER-2'
            P.move=False
        elif P.pos=='PRISECOUNTER-2':
            P.pos='GAMEAREA'
            P.move=False
        elif P.pos=='GAMEAREA':
            P.pos='MAINHALL'
            P.move=False
        elif P.pos=='MAINAHALL':
            P.pos='PARTYROOM4'
            P.move=False
        elif P.pos=='PARTYTROOM4':
            P.pos='PARTYROOM2'
            P.move=False
        elif P.pos=='PARTYROOM2' and office.maskTime==0:
            P.pos='IN-OFFICE'
            WF.move=False
def GoldenFreddyHallAi():
    chance=random.randint(1,10)
    if GF.ai>0 and office.side!='FRONT' and player.camsUp:
        if chance==1 and TC.pos!='OFFICE-HALLWAY' and TF.pos!='OFFICE-HALL1' and TF.pos!='OFFICE-HALL2' and WB.pos!='OFFICE-HALL' and WF.pos!='OFFICE-HALL' and MA.pos!='OFFICE-HALL' and WFO.pos!='OFFICE-HALL':
            GF.pos='OFFICE-HALL'
def GoldenFreddyOfficeAi():
    mChance=random.randint(1,20)
    if(GF.ai>=mChance):
        if GF.pos!='OFFICE-HALL' and player.camsUp:
            GF.pos='IN-OFFICE'
def setUpSFX():
    sfx.fansound = pygame.mixer.Sound('fansound.MP3')
    sfx.ambience2 = pygame.mixer.Sound('ambience2.MP3')
    sfx.blip = pygame.mixer.Sound('blip3.MP3')
    sfx.buzzlight = pygame.mixer.Sound('buzzlight.MP3')
    sfx.call1 = pygame.mixer.Sound('call 1b.MP3')
    sfx.call2 = pygame.mixer.Sound('call 2b.MP3')
    sfx.call3 = pygame.mixer.Sound('call 3b.MP3')
    sfx.call4 = pygame.mixer.Sound('call 4b.MP3')
    sfx.call5 = pygame.mixer.Sound('call 5b.MP3')
    sfx.call6 = pygame.mixer.Sound('call 6b.MP3')
    sfx.clockchimes = pygame.mixer.Sound('Clocks_Chimes_Cl_02480702.MP3')
    sfx.camBackground = pygame.mixer.Sound('CMPTR_Low_Tech_Stat.MP3')
    sfx.blip2 = pygame.mixer.Sound('COMPUTER_DIGITAL_L2076605.MP3')
    sfx.computerIntior = pygame.mixer.Sound('ComputerInteriorLong_EVL02_14.MP3')
    sfx.children = pygame.mixer.Sound('CROWD_SMALL_CHIL_EC049202.MP3')
    sfx.maskbreaths = pygame.mixer.Sound('deepbreaths.MP3')
    sfx.hi = pygame.mixer.Sound('echo1.MP3')
    sfx.hello = pygame.mixer.Sound('echo3b.MP3')
    sfx.laugh = pygame.mixer.Sound('echo4b.MP3')
    sfx.garble = pygame.mixer.Sound('elec garble.MP3')
    sfx.error = pygame.mixer.Sound('error.MP3')
    sfx.maskon = pygame.mixer.Sound('FENCING_42_GEN-HDF10953.MP3')
    sfx.maskoff = pygame.mixer.Sound('FENCING_43_GEN-HDF10954.MP3')
    sfx.ambience1 = pygame.mixer.Sound('In_The_Depths_C.MP3')
    sfx.jackinthebox = pygame.mixer.Sound('jackinthebox.MP3')
    sfx.machineturn = pygame.mixer.Sound('machineturn2.MP3')
    sfx.metalrun = pygame.mixer.Sound('metalrun.MP3')
    sfx.metalwalk1 = pygame.mixer.Sound('metalwalk1.MP3')
    sfx.metalwalk2 = pygame.mixer.Sound('metalwalk2.MP3')
    sfx.metalwalk2 = pygame.mixer.Sound('metalwalk3.MP3')
    sfx.musicbox = pygame.mixer.Sound('Music_Box_Melody_Playful.MP3')
    sfx.musicbox.set_volume(0.3)
    sfx.musicbox2 = pygame.mixer.Sound('musicbox2.MP3')
    sfx.pop = pygame.mixer.Sound('pop.MP3')
    sfx.popstatic = pygame.mixer.Sound('popstatic.MP3')
    sfx.arr = pygame.mixer.Sound('Robot.MP3')
    sfx.ambience3 = pygame.mixer.Sound('Scary_Space_B.MP3')
    sfx.stare = pygame.mixer.Sound('stare.MP3')
    sfx.death2 = pygame.mixer.Sound('static2.MP3')
    sfx.staticend = pygame.mixer.Sound('staticend2.MP3')
    sfx.camup = pygame.mixer.Sound('STEREO_CASSETTE__90097701.MP3')
    sfx.camdown = pygame.mixer.Sound('STEREO_CASSETTE__90097704.MP3')
    sfx.menumusic = pygame.mixer.Sound('The_Sand_Temple_Loop_G.MP3')
    sfx.ventwalk = pygame.mixer.Sound('ventwalk1.MP3')
    sfx.walk1 = pygame.mixer.Sound('walk1.MP3')
    sfx.walk2 = pygame.mixer.Sound('walk2.MP3')
    sfx.walk3 = pygame.mixer.Sound('walk3.MP3')
    sfx.walk4 = pygame.mixer.Sound('walk4.MP3')
    sfx.walk5 = pygame.mixer.Sound('walk5.MP3')
    sfx.windup = pygame.mixer.Sound('windup2.MP3')
    sfx.ambiencescary = pygame.mixer.Sound('With_S2.MP3')
    sfx.js1 = pygame.mixer.Sound('Xscream2.MP3')
    sfx.js2 = pygame.mixer.Sound('Xscream3.MP3')

def setupOfficeInts():
    global leftOff ,leftOn, rightOff , rightOn ,toybonnie , goldenfreddy , toychica ,  toyfreddy ,blackscreen, maskButton , camButton ,nightText , amText , flashlightText, mask1 , mask2 , mask3 , mask4 , mask5 , mask6 , mask7 , mask8 , mask9 ,mask10 ,desk1 , desk2 , desk3 , desk4
    
    office.image = officeImages['ONN']
    office.rect = office.image.get_rect()
    office.rect.y = 0
    office.rect.x = 0
    office.dx=0
    office.side='NONE' #Which was the camera is turning(helps keeps objects in sync when moving)
    office.light='NONE' #Current light that is on , only one can be on at a time. The states it can be are 'NONE' , 'LEFT' , 'RIGHT' , 'FRONT'
    office.deskFrame=0 #Frame number for desk animation
    office.maskFrame=0 #Frame number for mask animation
    office.inside=False #if an animatronic is inside the office , helps with use of mask and killing of the player
    office.maskTime=0 #timer for how long the mask needs to be on when an animatronic is in the room
    office.hallfull=False #if any animatroinics are in the hallway
    office.maskTimer=50 #Timer for how fast you need to put the mask on when an animatronic enters the room
    
    #light buttons
    leftOff=pygame.sprite.Sprite(officeInts)
    leftOff.image=officeIntImages['LEFT-OFF']
    leftOff.rect=leftOff.image.get_rect()
    leftOff.rect.x=WIDTH/13.241
    leftOff.rect.y=HEIGHT/1.901
    leftOff.dx=0
    
    leftOn=pygame.sprite.Sprite(officeInts)
    leftOn.image=officeIntImages['LEFT-ON']
    leftOn.rect=leftOn.image.get_rect()
    leftOn.rect.x=WIDTH/13.241
    leftOn.rect.y=HEIGHT/1.898
    leftOn.dx=0
    
    rightOff=pygame.sprite.Sprite(officeInts)
    rightOff.image=officeIntImages['RIGHT-OFF']
    rightOff.rect=rightOff.image.get_rect()
    rightOff.rect.x=WIDTH/.943
    rightOff.rect.y=HEIGHT/1.901
    rightOff.dx=0
    
    rightOn=pygame.sprite.Sprite(officeInts)
    rightOn.image=officeIntImages['RIGHT-ON']
    rightOn.rect=rightOn.image.get_rect()
    rightOn.rect.x=WIDTH/.943
    rightOn.rect.y=HEIGHT/1.901
    rightOn.dx=0
    #UI
    maskButton=pygame.sprite.Sprite(officeInts)
    maskButton.image=officeIntImages['MASK-BUTTON']
    maskButton.rect=maskButton.image.get_rect()
    maskButton.rect.x=WIDTH/38.4
    maskButton.rect.y=HEIGHT/1.09
    maskButton.image.set_alpha(100)
    
    
    camButton=pygame.sprite.Sprite(officeInts)
    camButton.image=officeIntImages['CAM-BUTTON']
    camButton.rect=camButton.image.get_rect()
    camButton.rect.x=WIDTH/1.979
    camButton.rect.y=HEIGHT/1.09
    camButton.image.set_alpha(100)
    #Texts
    nightText=pygame.sprite.Sprite(officeInts)
    nightText.image=officeIntImages['TEXT-NIGHT']
    nightText.rect=camButton.image.get_rect()
    nightText.rect.x=WIDTH/1.163
    nightText.rect.y=HEIGHT/36
    
    amText=pygame.sprite.Sprite(officeInts)
    amText.image=officeIntImages['TEXT-AM']
    amText.rect=camButton.image.get_rect()
    amText.rect.x=WIDTH/1.06
    amText.rect.y=HEIGHT/12
    
    flashlightText=pygame.sprite.Sprite(officeInts)
    flashlightText.image=officeIntImages['TEXT-FLASHLIGHT']
    flashlightText.rect=flashlightText.image.get_rect()
    flashlightText.rect.x=WIDTH/29.538                 
    flashlightText.rect.y=HEIGHT/43.2
    
    #Flashligh battery icons
    flashlight.image=officeIntImages['FLASHLIGHT-1']
    flashlight.rect=flashlight.image.get_rect()
    flashlight.rect.x=WIDTH/38.4
    flashlight.rect.y=HEIGHT/28
    
    #Mask animation frames
    
    mask.image=officeIntImages['MASK-F1']
    mask.rect=mask.image.get_rect()
    mask.rect.x=0
    mask.rect.y=HEIGHT/-7.2
    
    monitor.image=officeIntImages['CAM-F1']
    monitor.rect=monitor.image.get_rect()
    monitor.rect.x=0
    monitor.rect.y=HEIGHT/-7.2
    
    goldenfreddy=pygame.sprite.Sprite(officeInts)
    goldenfreddy.image=animatronicImages['ANIM-GF/OFFICE']
    goldenfreddy.rect=goldenfreddy.image.get_rect()
    goldenfreddy.rect.x=400
    goldenfreddy.rect.y=390
    goldenfreddy.dx=0
    
    #Toy bonnie cutout
    toybonnie=pygame.sprite.Sprite(officeInts)
    toybonnie.image=animatronicImages['ANIM-TB/OFFICE']
    toybonnie.rect=toybonnie.image.get_rect()
    toybonnie.rect.x=WIDTH/1.3714
    toybonnie.rect.y=HEIGHT/-21.6
    toybonnie.dx=0
    
    toychica=pygame.sprite.Sprite(officeInts)
    toychica.image=animatronicImages['ANIM-TC/OFFICE']
    toychica.rect=toybonnie.image.get_rect()
    toychica.rect.x=0
    toychica.rect.y=0
    toychica.dx=0
    
    toyfreddy=pygame.sprite.Sprite(officeInts)
    toyfreddy.image=animatronicImages['ANIM-TF/OFFICE']
    toyfreddy.rect=toyfreddy.image.get_rect()
    toyfreddy.rect.x=WIDTH/1.536
    toyfreddy.rect.y=HEIGHT/10.8
    toyfreddy.dx=0
    
    blackscreen=pygame.sprite.Sprite(officeInts)
    blackscreen.image=animatronicImages['ANIM-BLACKSCREEN']
    blackscreen.rect=blackscreen.image.get_rect()
    blackscreen.rect.x=0
    blackscreen.rect.y=0
    blackscreen.opacity=0 
    blackscreen.image.set_alpha(blackscreen.opacity)
    
    
    desk1=pygame.sprite.Sprite(officeDesks)
    desk1.image=officeDeskImages['DESK-F1']
    desk1.rect=desk1.image.get_rect()
    desk1.rect.x=WIDTH/3.49
    desk1.rect.y=HEIGHT/1.974
    desk1.dx=0
    
    desk2=pygame.sprite.Sprite(officeDesks)
    desk2.image=officeDeskImages['DESK-F2']
    desk2.rect=desk2.image.get_rect()
    desk2.rect.x=WIDTH/3.49
    desk2.rect.y=HEIGHT/1.974
    desk2.dx=0
    
    desk3=pygame.sprite.Sprite(officeDesks)
    desk3.image=officeDeskImages['DESK-F3']
    desk3.rect=desk3.image.get_rect()
    desk3.rect.x=WIDTH/3.49
    desk3.rect.y=HEIGHT/1.974
    desk3.dx=0
    
    desk4=pygame.sprite.Sprite(officeDesks)
    desk4.image=officeDeskImages['DESK-F4']
    desk4.rect=desk4.image.get_rect()
    desk4.rect.x=WIDTH/3.49
    desk4.rect.y=HEIGHT/1.974
    desk4.dx=0
    
def setupCams():
    global camMap , camOutline , camDot , manglePC , mangleGA , mangleMH , mangleP2 , mangleO , musicButtonOff , musicButtonOn , textWindUp , textClick , cambox1 , cambox2 , cambox3 , cambox4 , cambox5 , cambox6 , cambox7 , cambox8 ,cambox9 , cambox10 , cambox11 , cambox12 , Text01 , Text02 , Text03 , Text04 , Text05 , Text06 , Text06 , Text07 , Text08 , Text09 , Text10 , Text11 , Text12 , camGbox
    cam.image=camImages['SHOWSTAGE-FULL/N']
    cam.rect=cam.image.get_rect()
    cam.rect.x=0
    cam.rect.y=0
    cam.dx=3
    cam.move='LEFT' #which way the camera is moving
    cam.flash=False #if the flashlight is on in cameras
    cam.moveTimer=0 #timer for the movement of animatronics
    cam.puppetMoveTimer=0
    cam.staticTimer=0 #timer for camrea static when animatronics move
    
    textCam.image=camUIImages['TEXT-SHOWSTAGE']
    textCam.rect=textCam.image.get_rect()
    textCam.rect.x=WIDTH/1.794
    textCam.rect.y=HEIGHT/2.842
    
    static.image=overlayImages['STATIC1']
    static.rect=static.image.get_rect()
    static.rect.x=0
    static.rect.y=0
    
    
    camMap=pygame.sprite.Sprite(camUI)
    camMap.image=camUIImages['CAM-MAP']
    camMap.rect=camMap.image.get_rect()
    camMap.rect.x=WIDTH/1.828
    camMap.rect.y=HEIGHT/2.571
    
    camOutline=pygame.sprite.Sprite(camUI)
    camOutline.image=camUIImages['CAM-OUTLINE']
    camOutline.rect=camOutline.image.get_rect()
    camOutline.rect.x=0
    camOutline.rect.y=0
    
    cambox1=pygame.sprite.Sprite(camUI)
    cambox1.image=camUIImages['CAM-BOX']
    cambox1.rect=cambox1.image.get_rect()
    cambox1.rect.x=WIDTH/1.745
    cambox1.rect.y=HEIGHT/1.46
    
    cambox2=pygame.sprite.Sprite(camUI)
    cambox2.image=camUIImages['CAM-BOX']
    cambox2.rect=cambox2.image.get_rect()
    cambox2.rect.x=WIDTH/1.43
    cambox2.rect.y=HEIGHT/1.46
    
    cambox3=pygame.sprite.Sprite(camUI)
    cambox3.image=camUIImages['CAM-BOX']
    cambox3.rect=cambox3.image.get_rect()
    cambox3.rect.x=WIDTH/1.745
    cambox3.rect.y=HEIGHT/1.741
    
    cambox4=pygame.sprite.Sprite(camUI)
    cambox4.image=camUIImages['CAM-BOX']
    cambox4.rect=cambox4.image.get_rect()
    cambox4.rect.x=WIDTH/1.43
    cambox4.rect.y=HEIGHT/1.741
    
    cambox5=pygame.sprite.Sprite(camUI)
    cambox5.image=camUIImages['CAM-BOX']
    cambox5.rect=cambox5.image.get_rect()
    cambox5.rect.x=WIDTH/1.745
    cambox5.rect.y=HEIGHT/1.22
    
    cambox6=pygame.sprite.Sprite(camUI)
    cambox6.image=camUIImages['CAM-BOX']
    cambox6.rect=cambox6.image.get_rect()
    cambox6.rect.x=WIDTH/1.443
    cambox6.rect.y=HEIGHT/1.22
    
    cambox7=pygame.sprite.Sprite(camUI)
    cambox7.image=camUIImages['CAM-BOX']
    cambox7.rect=cambox7.image.get_rect()
    cambox7.rect.x=WIDTH/1.391
    cambox7.rect.y=HEIGHT/2.07
    
    cambox8=pygame.sprite.Sprite(camUI)
    cambox8.image=camUIImages['CAM-BOX']
    cambox8.rect=cambox8.image.get_rect()
    cambox8.rect.x=WIDTH/1.745
    cambox8.rect.y=HEIGHT/2.16
    
    cambox9=pygame.sprite.Sprite(camUI)
    cambox9.image=camUIImages['CAM-BOX']
    cambox9.rect=cambox9.image.get_rect()
    cambox9.rect.x=WIDTH/1.13
    cambox9.rect.y=HEIGHT/2.37
    
    cambox10=pygame.sprite.Sprite(camUI)
    cambox10.image=camUIImages['CAM-BOX']
    cambox10.rect=cambox10.image.get_rect()
    cambox10.rect.x=WIDTH/1.24
    cambox10.rect.y=HEIGHT/1.648
    
    cambox11=pygame.sprite.Sprite(camUI)
    cambox11.image=camUIImages['CAM-BOX']
    cambox11.rect=cambox10.image.get_rect()
    cambox11.rect.x=WIDTH/1.09
    cambox11.rect.y=HEIGHT/1.92
    
    cambox12=pygame.sprite.Sprite(camUI)
    cambox12.image=camUIImages['CAM-BOX']
    cambox12.rect=cambox10.image.get_rect()
    cambox12.rect.x=WIDTH/1.129
    cambox12.rect.y=HEIGHT/1.469
    
    Text01=pygame.sprite.Sprite(camUI)
    Text01.image=camUIImages['TEXT-CAM01']
    Text01.rect=Text01.image.get_rect()
    Text01.rect.x=WIDTH/1.729
    Text01.rect.y=HEIGHT/1.44
    
    Text02=pygame.sprite.Sprite(camUI)
    Text02.image=camUIImages['TEXT-CAM02']
    Text02.rect=Text02.image.get_rect()
    Text02.rect.x=WIDTH/1.421
    Text02.rect.y=HEIGHT/1.44
    
    Text03=pygame.sprite.Sprite(camUI)
    Text03.image=camUIImages['TEXT-CAM03']
    Text03.rect=Text03.image.get_rect()
    Text03.rect.x=WIDTH/1.729
    Text03.rect.y=HEIGHT/1.714
    
    Text04=pygame.sprite.Sprite(camUI)
    Text04.image=camUIImages['TEXT-CAM04']
    Text04.rect=Text04.image.get_rect()
    Text04.rect.x=WIDTH/1.421
    Text04.rect.y=HEIGHT/1.714
    
    Text05=pygame.sprite.Sprite(camUI)
    Text05.image=camUIImages['TEXT-CAM05']
    Text05.rect=Text05.image.get_rect()
    Text05.rect.x=WIDTH/1.729
    Text05.rect.y=HEIGHT/1.206
    
    Text06=pygame.sprite.Sprite(camUI)
    Text06.image=camUIImages['TEXT-CAM06']
    Text06.rect=Text06.image.get_rect()
    Text06.rect.x=WIDTH/1.432
    Text06.rect.y=HEIGHT/1.206
    
    Text07=pygame.sprite.Sprite(camUI)
    Text07.image=camUIImages['TEXT-CAM07']
    Text07.rect=Text07.image.get_rect()
    Text07.rect.x=WIDTH/1.381
    Text07.rect.y=HEIGHT/2.03
    
    Text08=pygame.sprite.Sprite(camUI)
    Text08.image=camUIImages['TEXT-CAM08']
    Text08.rect=Text08.image.get_rect()
    Text08.rect.x=WIDTH/1.729
    Text08.rect.y=HEIGHT/2.117
    
    Text09=pygame.sprite.Sprite(camUI)
    Text09.image=camUIImages['TEXT-CAM09']
    Text09.rect=Text09.image.get_rect()
    Text09.rect.x=WIDTH/1.124
    Text09.rect.y=HEIGHT/2.322
    
    Text10=pygame.sprite.Sprite(camUI)
    Text10.image=camUIImages['TEXT-CAM10']
    Text10.rect=Text10.image.get_rect()
    Text10.rect.x=WIDTH/1.233
    Text10.rect.y=HEIGHT/1.624
    
    Text11=pygame.sprite.Sprite(camUI)
    Text11.image=camUIImages['TEXT-CAM11']
    Text11.rect=Text11.image.get_rect()
    Text11.rect.x=WIDTH/1.084
    Text11.rect.y=HEIGHT/1.89
    
    Text12=pygame.sprite.Sprite(camUI)
    Text12.image=camUIImages['TEXT-CAM12']
    Text12.rect=Text12.image.get_rect()
    Text12.rect.x=WIDTH/1.122
    Text12.rect.y=HEIGHT/1.445
    
    camGbox=pygame.sprite.Sprite(camUI)
    camGbox.image=camUIImages['CAM-GBOX']
    camGbox.rect=camGbox.image.get_rect()
    camGbox.rect.x=cambox9.rect.x
    camGbox.rect.y=cambox9.rect.y
    
    camDot=pygame.sprite.Sprite(camUI)
    camDot.image=camUIImages['CAM-DOT']
    camDot.rect=camDot.image.get_rect()
    camDot.rect.x=WIDTH/29.53
    camDot.rect.y=HEIGHT/9.818
    
    musicButtonOff=pygame.sprite.Sprite(camUI)
    musicButtonOff.image=camUIImages['CAM-MUSICBUTTON_GREY']
    musicButtonOff.rect=musicButtonOff.image.get_rect()
    musicButtonOff.rect.x=WIDTH/3.2
    musicButtonOff.rect.y=HEIGHT/1.384
    
    musicButtonOn=pygame.sprite.Sprite(camUI)
    musicButtonOn.image=camUIImages['CAM-MUSICBUTTON_GREEN']
    musicButtonOn.rect=musicButtonOn.image.get_rect()
    musicButtonOn.rect.x=WIDTH/3.2
    musicButtonOn.rect.y=HEIGHT/1.384
    
    textWindUp=pygame.sprite.Sprite(camUI)
    textWindUp.image=camUIImages['TEXT-WIND/UP/MUSICBOX']
    textWindUp.rect=textWindUp.image.get_rect()
    textWindUp.rect.x=WIDTH/3.14
    textWindUp.rect.y=HEIGHT/1.35
    
    textClick=pygame.sprite.Sprite(camUI)
    textClick.image=camUIImages['TEXT-CLICK&HOLD']
    textClick.rect=textClick.image.get_rect()
    textClick.rect.x=WIDTH/3.2
    textClick.rect.y=HEIGHT/1.206
    
    musicBox.image=camUIImages['CAM-MUSIC_BAR21']
    musicBox.rect=musicBox.image.get_rect()
    musicBox.rect.x=WIDTH/4.465
    musicBox.rect.y=HEIGHT/1.375
    
    white.image=overlayImages['WHITE1']
    white.rect=white.image.get_rect()
    white.rect.x=0
    white.rect.y=0
    
    manglePC=pygame.sprite.Sprite(camUI)
    manglePC.image=animatronicImages['MANGLE-PRISECOUNTER']
    manglePC.rect=manglePC.image.get_rect()
    manglePC.rect.x=1100
    manglePC.rect.y=0
    
    mangleGA=pygame.sprite.Sprite(camUI)
    mangleGA.image=animatronicImages['MANGLE-GAMEAREA']
    mangleGA.rect=mangleGA.image.get_rect()
    mangleGA.rect.x=0
    mangleGA.rect.y=0
    
    mangleMH=pygame.sprite.Sprite(camUI)
    mangleMH.image=animatronicImages['MANGLE-MAINHALL']
    mangleMH.rect=mangleMH.image.get_rect()
    mangleMH.rect.x=1100
    mangleMH.rect.y=636
    
    mangleP2=pygame.sprite.Sprite(camUI)
    mangleP2.image=animatronicImages['MANGLE-PARTYROOM2']
    mangleP2.rect=mangleP2.image.get_rect()
    mangleP2.rect.x=0
    mangleP2.rect.y=300
    
    mangleO=pygame.sprite.Sprite(camUI)
    mangleO.image=animatronicImages['MANGLE-OFFICE']
    mangleO.rect=mangleO.image.get_rect()
    mangleO.rect.x=1100
    mangleO.rect.y=0
    mangleO.dx=0
    
    
    
def setUpAnimatronics():
    global TB , TC , TF , WB , WC , WF , WFO , MA , GF , BB , P
        #ANIMATRONICS
    #TOYBONNIE
    TB=pygame.sprite.Sprite() 
    TB.ai=10 #ai level
    TB.pos='SHOWSTAGE' #current location
    TB.move=False #if movechance alows it to move
    TB.attack=False #if they attack the player
    TB.frame=0 #frame for jumpscare
    TB.image=animatronicImages['ANIM-TB_JS1']
    TB.rect=TB.image.get_rect()
    TB.rect.x=0
    TB.rect.y=0
    
    #TOY CHICA
    TC=pygame.sprite.Sprite() 
    TC.ai=0
    TC.pos='SHOWSTAGE' 
    TC.move=False
    TC.attack=False
    TC.frame=0
    #TOY FREDDY
    TF=pygame.sprite.Sprite() 
    TF.ai=0 
    TF.pos='SHOWSTAGE' 
    TF.move=False
    TF.attack=False
    TF.frame=0
    #WITHERED BONNIE
    WB=pygame.sprite.Sprite() 
    WB.ai=0
    WB.pos='P&S' 
    WB.move=False
    WB.attack=False
    WB.frame=0
    #WITHERED CHICA
    WC=pygame.sprite.Sprite() 
    WC.ai=0
    WC.pos='P&S' 
    WC.move=False
    WC.attack=False
    WC.frame=0
    #WITHERED FREDDY
    WF=pygame.sprite.Sprite() 
    WF.ai=0
    WF.pos='P&S' 
    WF.move=False
    WF.attack=False
    WF.frame=0
    #WITHERED FOXY
    WFO=pygame.sprite.Sprite() 
    WFO.ai=0
    WFO.pos='P&S' 
    WFO.move=False
    WFO.valueTimer=0
    WFO.value=0
    WFO.attackTimer=0
    WFO.attack=False
    WFO.frame=0
    #BALLOON BOY
    BB=pygame.sprite.Sprite() 
    BB.ai=0
    BB.pos='GAMEAREA' 
    BB.move=False
    BB.timer=0
    #GOLDEN FREDDY
    GF=pygame.sprite.Sprite() 
    GF.ai=0
    GF.pos='N/A' 
    GF.timer=0 #timer for his hallway ai
    GF.value=0 #value which helps determine if he kills you when hes in the hall
    GF.increase=False #if the value is increasing
    GF.seen=False #if you have seen him in the office/hall
    GF.attack=False
    GF.frame=0
    #MANGLE
    MA=pygame.sprite.Sprite() 
    MA.ai=0
    MA.pos='KIDSCOVE' 
    MA.move=False
    MA.timer=0 #timer for how long its in office before it kills you
    MA.attack=False
    MA.frame=0
    #PUPPET
    P=pygame.sprite.Sprite() 
    P.ai=0
    P.timertimer=0 #second timer for music box
    P.timer=2000 #Music box Timer
    P.subtraction=4 #the subtraction of time from the music box
    P.recharge=False #if the music box it being recharged or not
    P.move=False #if the puppet is moving 
    P.pos='PRISECOUNTER' # the pos of the puppet if out of the box
    P.out=False #if the puppet is out of the box
    P.attack=False
    P.frame=0
    
    
def loadOffice():
    global officeImages
    sheet = Spritesheet('office-SS.png')
    
    #[LEGEND]
    #N=NONE
    #O(office)
    #N(None/if a flashlight is on) 
    #N(None/name of animatroic)
    
    #OFFICE IMAGES
    officeImages={}
    officeImages['ONN'] = pygame.transform.scale(sheet.image_at((3206,2,1600,768)), (WIDTH*1.1718, HEIGHT))
    officeImages['OFN'] = pygame.transform.scale(sheet.image_at((4808,2,1600,768)), (WIDTH*1.1718, HEIGHT))
    officeImages['OLN'] = pygame.transform.scale(sheet.image_at((6410,2,1600,768)), (WIDTH*1.1718, HEIGHT))
    officeImages['ORN'] = pygame.transform.scale(sheet.image_at((8012,2,1600,768)), (WIDTH*1.1718, HEIGHT))
    #TOY FREDDY
    officeImages['OF_T-FREDDY1'] = pygame.transform.scale(sheet.image_at((4808,772,1600,768)), (WIDTH*1.1718, HEIGHT))
    officeImages['OF_T-FREDDY2'] = pygame.transform.scale(sheet.image_at((6410,772,1600,768)), (WIDTH*1.1718, HEIGHT))
    #TOY BONNIE
    officeImages['OR_T-BONNIE1'] = pygame.transform.scale(sheet.image_at((2,772,1600,768)), (WIDTH*1.1718, HEIGHT))
    #TOY CHICA
    officeImages['OF_T-CHICA1'] = pygame.transform.scale(sheet.image_at((1604,772,1600,768)), (WIDTH*1.1718, HEIGHT))
    officeImages['OL_T-CHICA2'] = pygame.transform.scale(sheet.image_at((1604,2,1600,768)), (WIDTH*1.1718, HEIGHT))
    #MANGLE
    officeImages['OF_MANGLE1'] = pygame.transform.scale(sheet.image_at((3206,772,1600,768)), (WIDTH*1.1718, HEIGHT))
    officeImages['OR_MANGLE2'] = pygame.transform.scale(sheet.image_at((8012,1542,1600,768)), (WIDTH*1.1718, HEIGHT))
    #BALOON BOY
    officeImages['OL_B-BOY'] = pygame.transform.scale(sheet.image_at((6410,1542,1600,768)), (WIDTH*1.1718, HEIGHT))
    #WITHERED FREDDY
    officeImages['OF_W-FREDDY1'] = pygame.transform.scale(sheet.image_at((3206,1542,1600,768)), (WIDTH*1.1718, HEIGHT))
    officeImages['ON_W-FREDDY2'] = pygame.transform.scale(sheet.image_at((2,2,1600,768)), (WIDTH*1.1718, HEIGHT))
    #WITHERED BONNIE
    officeImages['OF_W-BONNIE1'] = pygame.transform.scale(sheet.image_at((8012,772,1600,768)), (WIDTH*1.1718, HEIGHT))
    officeImages['ON_W-BONNIE2'] = pygame.transform.scale(sheet.image_at((2,1542,1600,768)), (WIDTH*1.1718, HEIGHT))
    #WITHERED CHICA
    officeImages['ON_W-CHICA'] = pygame.transform.scale(sheet.image_at((1604,1542,1600,768)), (WIDTH*1.1718, HEIGHT))
    #WITHERED FOXY
    officeImages['OF_W-FOXY1'] = pygame.transform.scale(sheet.image_at((4808,1542,1600,768)), (WIDTH*1.1718, HEIGHT))
    #GOLDEN FREDDY
    officeImages['OF_G-FREDDY'] = pygame.transform.scale(sheet.image_at((2,2312,1600,768)), (WIDTH*1.1718, HEIGHT))
    #W-FOXY & W-BONNIE
    officeImages['OF_W-FOXY/W-BONNIE'] = pygame.transform.scale(sheet.image_at((1604,2312,1600,768)), (WIDTH*1.1718, HEIGHT))
    #W-FOXY & MANGLE
    officeImages['OF_W-FOXY/W-MANGLE'] = pygame.transform.scale(sheet.image_at((3206,2312,1600,768)), (WIDTH*1.1718, HEIGHT))
    
def loadOfficeInteractives():
    global officeIntImages
    
    sheet = Spritesheet('office-Int-SS2.png')
    
    officeIntImages={}
    #Light buttons
    officeIntImages['LEFT-OFF']=pygame.transform.scale(sheet.image_at((10466,671,57,87), colorkey =(5,5,5)), (WIDTH/20.869*.75,HEIGHT/7.659*.75))
    officeIntImages['RIGHT-OFF']=pygame.transform.scale(sheet.image_at((10657,671,57,87), colorkey =(5,5,5)), (WIDTH/20.869*.75,HEIGHT/7.659*.75))
    officeIntImages['LEFT-ON']=pygame.transform.scale(sheet.image_at((10559,672,57,87), colorkey =(5,5,5)), (WIDTH/20.869*.75,HEIGHT/7.659*.75))
    officeIntImages['RIGHT-ON']=pygame.transform.scale(sheet.image_at((10750,671,57,87), colorkey =(5,5,5)), (WIDTH/20.869*.75,HEIGHT/7.659*.75))
    #THE UI
    #the buttons for mask/cams
    officeIntImages['MASK-BUTTON']=pygame.transform.scale(sheet.image_at((10460,880,481,39), colorkey =(5,5,5)), (WIDTH/2.13,HEIGHT/27*1.4))
    officeIntImages['CAM-BUTTON']=pygame.transform.scale(sheet.image_at((10460,838,481,39), colorkey =(5,5,5)), (WIDTH/2.13,HEIGHT/27*1.4))
    #Texts
    officeIntImages['TEXT-NIGHT']=pygame.transform.scale(sheet.image_at((10451,607,93,22), colorkey =(90,90,90)), (93*1.6,22*1.3))
    officeIntImages['TEXT-AM']=pygame.transform.scale(sheet.image_at((10545,607,36,22), colorkey =(90,90,90)), (36*1.6,22*1.3))
    officeIntImages['TEXT-FLASHLIGHT']=pygame.transform.scale(sheet.image_at((10582,617,86,12), colorkey =(90,90,90)), (86*1.6,12*1.3))
    #Flashlight battery power icons
    officeIntImages['FLASHLIGHT-1']=pygame.transform.scale(sheet.image_at((10451,787,100,50), colorkey =(0,0,0)), (WIDTH/12.8,HEIGHT/18))#full battery
    officeIntImages['FLASHLIGHT-2']=pygame.transform.scale(sheet.image_at((10552,787,100,50), colorkey =(0,0,0)), (WIDTH/12.8,HEIGHT/18))
    officeIntImages['FLASHLIGHT-3']=pygame.transform.scale(sheet.image_at((10653,787,100,50), colorkey =(0,0,0)), (WIDTH/12.8,HEIGHT/18))
    officeIntImages['FLASHLIGHT-4']=pygame.transform.scale(sheet.image_at((10754,787,100,50), colorkey =(0,0,0)), (WIDTH/12.8,HEIGHT/18))
    officeIntImages['FLASHLIGHT-5']=pygame.transform.scale(sheet.image_at((10855,787,100,50), colorkey =(0,0,0)), (WIDTH/12.8,HEIGHT/18))#completely depleted battery
    #Mask frames
    officeIntImages['MASK-F1']=pygame.transform.scale(sheet.image_at((1,151,1024,768), colorkey =(5,5,5)), (WIDTH,HEIGHT/.75))
    officeIntImages['MASK-F2']=pygame.transform.scale(sheet.image_at((1026,151,1024,768), colorkey =(5,5,5)), (WIDTH,HEIGHT/.75))
    officeIntImages['MASK-F3']=pygame.transform.scale(sheet.image_at((2051,151,1024,768), colorkey =(5,5,5)), (WIDTH,HEIGHT/.75))
    officeIntImages['MASK-F4']=pygame.transform.scale(sheet.image_at((3076,151,1024,768), colorkey =(5,5,5)), (WIDTH,HEIGHT/.75))
    officeIntImages['MASK-F5']=pygame.transform.scale(sheet.image_at((4101,151,1024,768), colorkey =(5,5,5)), (WIDTH,HEIGHT/.75))
    officeIntImages['MASK-F6']=pygame.transform.scale(sheet.image_at((5126,151,1024,768), colorkey =(5,5,5)), (WIDTH,HEIGHT/.75))
    officeIntImages['MASK-F7']=pygame.transform.scale(sheet.image_at((6151,151,1024,768), colorkey =(5,5,5)), (WIDTH,HEIGHT/.75))
    officeIntImages['MASK-F8']=pygame.transform.scale(sheet.image_at((7176,151,1024,768), colorkey =(5,5,5)), (WIDTH,HEIGHT/.75))
    officeIntImages['MASK-F9']=pygame.transform.scale(sheet.image_at((8201,151,1024,768), colorkey =(5,5,5)), (WIDTH,HEIGHT/.75))
    
    
def loadCameraFrames():
    
    sheet=Spritesheet('office-Int-SS.png')
    #Camera frames
    officeIntImages['CAM-F1']=pygame.transform.scale(sheet.image_at((1,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F2']=pygame.transform.scale(sheet.image_at((1026,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F3']=pygame.transform.scale(sheet.image_at((2051,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F4']=pygame.transform.scale(sheet.image_at((3076,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F5']=pygame.transform.scale(sheet.image_at((4101,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F6']=pygame.transform.scale(sheet.image_at((5126,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F7']=pygame.transform.scale(sheet.image_at((6151,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F8']=pygame.transform.scale(sheet.image_at((7176,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F9']=pygame.transform.scale(sheet.image_at((8201,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F10']=pygame.transform.scale(sheet.image_at((9226,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
    officeIntImages['CAM-F11']=pygame.transform.scale(sheet.image_at((10251,920,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT/.75))
def loadOfficeDesk():
    global officeDeskImages
    sheet=Spritesheet('office-Desk-SS.png')
    officeDeskImages={}
    officeDeskImages['DESK-F1']=pygame.transform.scale(sheet.image_at((9,12,851,435), colorkey =(11,11,11)), (WIDTH/1.84*1.1618,HEIGHT/2.026))
    officeDeskImages['DESK-F2']=pygame.transform.scale(sheet.image_at((9,462,851,435), colorkey =(11,11,11)), (WIDTH/1.84*1.1618,HEIGHT/2.026))
    officeDeskImages['DESK-F3']=pygame.transform.scale(sheet.image_at((884,12,851,435), colorkey =(11,11,11)), (WIDTH/1.84*1.1618,HEIGHT/2.026))
    officeDeskImages['DESK-F4']=pygame.transform.scale(sheet.image_at((886,463,851,435), colorkey =(11,11,11)), (WIDTH/1.84*1.1618,HEIGHT/2.026))
def loadShowStageCam():
    global camImages
    
    sheet=Spritesheet('cams-ShowStage-SS.png')
    
    camImages={}
    camImages['SHOWSTAGE-FULL/N']=pygame.transform.scale(sheet.image_at((2,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['SHOWSTAGE-FULL/L']=pygame.transform.scale(sheet.image_at((1604,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['SHOWSTAGE-F&C/N']=pygame.transform.scale(sheet.image_at((3206,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['SHOWSTAGE-F&C/L']=pygame.transform.scale(sheet.image_at((4808,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['SHOWSTAGE-F/N']=pygame.transform.scale(sheet.image_at((6410,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['SHOWSTAGE-F/L']=pygame.transform.scale(sheet.image_at((8012,2,1600,768)), (WIDTH*1.1718,HEIGHT))                                                        
    camImages['SHOWSTAGE-EMPTY']=pygame.transform.scale(sheet.image_at((2,772,1600,768)), (WIDTH*1.1718,HEIGHT))                                                      
    
def loadGameAreaCam():
                                                          
    sheet=Spritesheet('cams-GameArea-SS.png')
                                                              
    camImages['GAMEAREA-BB/N']=pygame.transform.scale(sheet.image_at((2,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['GAMEAREA-BB/L']=pygame.transform.scale(sheet.image_at((1604,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['GAMEAREA-EMPTY/N']=pygame.transform.scale(sheet.image_at((3206,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['GAMEAREA-EMPTY/L']=pygame.transform.scale(sheet.image_at((4808,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['GAMEAREA-BB&F/L']=pygame.transform.scale(sheet.image_at((6410,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['GAMEAREA-F/L']=pygame.transform.scale(sheet.image_at((8012,2,1600,768)), (WIDTH*1.1718,HEIGHT))
                                                           

def loadkidsCoveCam():
                                                       
    sheet=Spritesheet('cams-kidsCove-SS.png')
      
    camImages['KIDSCOVE-EMPTY/L']=pygame.transform.scale(sheet.image_at((2,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['KIDSCOVE-EMPTY/N']=pygame.transform.scale(sheet.image_at((1604,2,1600,768)), (WIDTH*1.1718,HEIGHT))                                                       
    camImages['KIDSCOVE-M/L']=pygame.transform.scale(sheet.image_at((3206,2,1600,768)), (WIDTH*1.1718,HEIGHT))

def loadPriseCornerCam():
                                                       
    sheet=Spritesheet('cams-PriseCorner-SS.png')
        
    camImages['PRISECOUNTER-M1/L']=pygame.transform.scale(sheet.image_at((2,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PRISECOUNTER-M2/L']=pygame.transform.scale(sheet.image_at((1604,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PRISECOUNTER-M3/L']=pygame.transform.scale(sheet.image_at((3206,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PRISECOUNTER-EMPTY/L']=pygame.transform.scale(sheet.image_at((4808,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PRISECOUNTER-EMPTY/N']=pygame.transform.scale(sheet.image_at((6410,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PRISECOUNTER-ENDO/L']=pygame.transform.scale(sheet.image_at((8012,2,1600,768)), (WIDTH*1.1718,HEIGHT))


def loadMainHallCam():
                                                           
    sheet=Spritesheet('cams-MainHall-SS.png')

    camImages['MAINHALL-EMPTY/N']=pygame.transform.scale(sheet.image_at((2,2,1600,768)), (WIDTH*1.1718,HEIGHT))                                                               
    camImages['MAINHALL-EMPTY/L']=pygame.transform.scale(sheet.image_at((1604,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['MAINHALL-WB/L']=pygame.transform.scale(sheet.image_at((3206,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['MAINHALL-WF/L']=pygame.transform.scale(sheet.image_at((4808,2,1600,768)), (WIDTH*1.1718,HEIGHT))  
    camImages['MAINHALL-TC/N']=pygame.transform.scale(sheet.image_at((6410,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['MAINHALL-TC/L']=pygame.transform.scale(sheet.image_at((8012,2,1600,768)), (WIDTH*1.1718,HEIGHT))
                                                           
def loadPartsandServiceCam():
                                                           
    sheet=Spritesheet('cams-PartsAndService-SS.png')
    
    camImages['P&S-FULL/N']=pygame.transform.scale(sheet.image_at((3005,558,10,10)), (WIDTH*1.1718,HEIGHT)) 
    camImages['P&S-FULL/L']=pygame.transform.scale(sheet.image_at((2,2,1600,768)), (WIDTH*1.1718,HEIGHT))                                                               
    camImages['P&S-WF&WC/L']=pygame.transform.scale(sheet.image_at((1604,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['P&S-WF/L']=pygame.transform.scale(sheet.image_at((3206,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['P&S-EMPTY/L']=pygame.transform.scale(sheet.image_at((4808,2,1600,768)), (WIDTH*1.1718,HEIGHT))  
    camImages['P&S-WFOXY/L']=pygame.transform.scale(sheet.image_at((6410,2,1600,768)), (WIDTH*1.1718,HEIGHT))
    camImages['P&S-SF/L']=pygame.transform.scale(sheet.image_at((8012,2,1600,768)), (WIDTH*1.1718,HEIGHT))

def loadPartyRoom1Cam():
                                                           
    sheet=Spritesheet('cams-PartyRoom1-SS.png')

    camImages['PARTYROOM1-EMPTY/N']=pygame.transform.scale(sheet.image_at((1,1,1024,768)), (WIDTH*1.1718,HEIGHT))                                                               
    camImages['PARTYROOM1-EMPTY/L']=pygame.transform.scale(sheet.image_at((1026,1,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM1-TC/L']=pygame.transform.scale(sheet.image_at((1,770,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM1-WB/L']=pygame.transform.scale(sheet.image_at((1026,770,1024,768)), (WIDTH*1.1718,HEIGHT))  

def loadPartyRoom2Cam():
                                                           
    sheet=Spritesheet('cams-PartyRoom2-SS.png')
    
    camImages['PARTYROOM2-EMPTY/N']=pygame.transform.scale(sheet.image_at((1,1,1024,768)), (WIDTH*1.1718,HEIGHT))                                                               
    camImages['PARTYROOM2-EMPTY/L']=pygame.transform.scale(sheet.image_at((1026,1,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM2-WC/N']=pygame.transform.scale(sheet.image_at((1,770,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM2-WC/L']=pygame.transform.scale(sheet.image_at((1026,770,1024,768)), (WIDTH*1.1718,HEIGHT)) 
    camImages['PARTYROOM2-TB/L']=pygame.transform.scale(sheet.image_at((2051,770,1024,768)), (WIDTH*1.1718,HEIGHT))
                                                               
def loadPartyRoom3Cam():
                                                           
    sheet=Spritesheet('cams-PartyRoom3-SS.png')
    
    
    camImages['PARTYROOM3-EMPTY/N']=pygame.transform.scale(sheet.image_at((1,1,1024,768)), (WIDTH*1.1718,HEIGHT))                                                               
    camImages['PARTYROOM3-EMPTY/L']=pygame.transform.scale(sheet.image_at((1026,1,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM3-WF/N']=pygame.transform.scale(sheet.image_at((1,770,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM3-WF/L']=pygame.transform.scale(sheet.image_at((1026,770,1024,768)), (WIDTH*1.1718,HEIGHT)) 
    camImages['PARTYROOM3-TB/L']=pygame.transform.scale(sheet.image_at((2051,770,1024,768)), (WIDTH*1.1718,HEIGHT))
                                               
def loadPartyRoom4Cam():
                                                        
    sheet=Spritesheet('cams-PartyRoom4-SS.png')
    
    
    camImages['PARTYROOM4-EMPTY/N']=pygame.transform.scale(sheet.image_at((1,1,1024,768)), (WIDTH*1.1718,HEIGHT))                                                               
    camImages['PARTYROOM4-EMPTY/L']=pygame.transform.scale(sheet.image_at((1026,1,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM4-EMPTY2/L']=pygame.transform.scale(sheet.image_at((2051,1,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM4-TB/N']=pygame.transform.scale(sheet.image_at((1,770,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM4-TB/L']=pygame.transform.scale(sheet.image_at((1026,770,1024,768)), (WIDTH*1.1718,HEIGHT)) 
    camImages['PARTYROOM4-TC/L']=pygame.transform.scale(sheet.image_at((2051,770,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['PARTYROOM4-WC/L']=pygame.transform.scale(sheet.image_at((3076,770,1024,768)), (WIDTH*1.1718,HEIGHT))                                           

def loadVentCams():
                                                        
    sheet=Spritesheet('cams-Vents-SS.png')
    
    camImages['LEFTVENT-EMPTY/N']=pygame.transform.scale(sheet.image_at((2048,0,1024,768)), (WIDTH*1.1718,HEIGHT))                                                               
    camImages['LEFTVENT-EMPTY/L']=pygame.transform.scale(sheet.image_at((2,769,1024,768)), (WIDTH*1.1718,HEIGHT))                                          
    camImages['LEFTVENT-TC/L']=pygame.transform.scale(sheet.image_at((3072,0,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['LEFTVENT-BB/L']=pygame.transform.scale(sheet.image_at((1026,769,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['LEFTVENT-WB/L']=pygame.transform.scale(sheet.image_at((2,1537,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['LEFTVENT-ENDO/L']=pygame.transform.scale(sheet.image_at((2050,769,1024,768)), (WIDTH*1.1718,HEIGHT))
    
    camImages['RIGHTVENT-EMPTY/N']=pygame.transform.scale(sheet.image_at((0,1,1024,767)), (WIDTH*1.1718,HEIGHT))
    camImages['RIGHTVENT-EMPTY/L']=pygame.transform.scale(sheet.image_at((1024,0,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['RIGHTVENT-TB/L']=pygame.transform.scale(sheet.image_at((2050,1537,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['RIGHTVENT-WC/L']=pygame.transform.scale(sheet.image_at((1026,1537,1024,768)), (WIDTH*1.1718,HEIGHT))
    camImages['RIGHTVENT-M/L']=pygame.transform.scale(sheet.image_at((3075,769,1022,768)), (WIDTH*1.1718,HEIGHT))
    
def loadCamUI():
    global camUIImages
    sheet= Spritesheet('cams-UI-SS.png')
    
    camUIImages={}
    camUIImages['CAM-MAP']=pygame.transform.scale(sheet.image_at((2,2,414,310), colorkey =(5,5,5)), (WIDTH/2.56,HEIGHT/2.113))
    camUIImages['CAM-OUTLINE']=pygame.transform.scale(sheet.image_at((420,3,1022,766), colorkey =(5,5,5)), (WIDTH,HEIGHT))
    camUIImages['CAM-BOX']=pygame.transform.scale(sheet.image_at((296,315,60,40), colorkey =(5,5,5)), (WIDTH/18.823,HEIGHT/15.882))
    camUIImages['CAM-GBOX']=pygame.transform.scale(sheet.image_at((357,315,60,40), colorkey =(5,5,5)), (WIDTH/18.823,HEIGHT/15.882))
    camUIImages['TEXT-CAM01']=pygame.transform.scale(sheet.image_at((1,315,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM02']=pygame.transform.scale(sheet.image_at((1,341,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM03']=pygame.transform.scale(sheet.image_at((1,367,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM04']=pygame.transform.scale(sheet.image_at((1,393,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM05']=pygame.transform.scale(sheet.image_at((1,419,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM06']=pygame.transform.scale(sheet.image_at((1,445,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM07']=pygame.transform.scale(sheet.image_at((1,471,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM08']=pygame.transform.scale(sheet.image_at((1,497,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM09']=pygame.transform.scale(sheet.image_at((1,523,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM10']=pygame.transform.scale(sheet.image_at((1,549,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM11']=pygame.transform.scale(sheet.image_at((1,575,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    camUIImages['TEXT-CAM12']=pygame.transform.scale(sheet.image_at((1,601,31,25), colorkey =(90,90,90)), (WIDTH/32,HEIGHT/24))
    
    camUIImages['TEXT-PARTYROOM1']=pygame.transform.scale(sheet.image_at((33,318,223,22), colorkey =(90,90,90)), (WIDTH/5.680,HEIGHT/32.7272))
    camUIImages['TEXT-PARTYROOM2']=pygame.transform.scale(sheet.image_at((33,344,226,22), colorkey =(90,90,90)), (WIDTH/5.597,HEIGHT/32.7272))
    camUIImages['TEXT-PARTYROOM3']=pygame.transform.scale(sheet.image_at((33,370,226,22), colorkey =(90,90,90)), (WIDTH/5.597,HEIGHT/32.7272))
    camUIImages['TEXT-PARTYROOM4']=pygame.transform.scale(sheet.image_at((33,396,226,22), colorkey =(90,90,90)), (WIDTH/5.597,HEIGHT/32.7272))
    camUIImages['TEXT-LEFTAIRVENT']=pygame.transform.scale(sheet.image_at((33,422,245,22), colorkey =(90,90,90)), (WIDTH/5.630,HEIGHT/32.7272))
    camUIImages['TEXT-RIGHTAIRVENT']=pygame.transform.scale(sheet.image_at((33,448,264,22), colorkey =(90,90,90)), (WIDTH/4.8,HEIGHT/32.7272))
    camUIImages['TEXT-MAINHALL']=pygame.transform.scale(sheet.image_at((33,474,166,22), colorkey =(90,90,90)), (WIDTH/7.619,HEIGHT/32.7272))
    camUIImages['TEXT-P&S']=pygame.transform.scale(sheet.image_at((33,500,245,22), colorkey =(90,90,90)), (WIDTH/5.161,HEIGHT/32.7272))
    camUIImages['TEXT-SHOWSTAGE']=pygame.transform.scale(sheet.image_at((33,526,188,22), colorkey =(90,90,90)), (WIDTH/6.736,HEIGHT/32.7272))
    camUIImages['TEXT-GAMEAREA']=pygame.transform.scale(sheet.image_at((33,552,169,22), colorkey =(90,90,90)), (WIDTH/7.5,HEIGHT/32.7272))
    camUIImages['TEXT-PRISECOUNTER']=pygame.transform.scale(sheet.image_at((33,578,226,22), colorkey =(90,90,90)), (WIDTH/5.597,HEIGHT/32.7272))
    camUIImages['TEXT-KIDSCOVE']=pygame.transform.scale(sheet.image_at((33,604,188,22), colorkey =(90,90,90)), (WIDTH/6.736,HEIGHT/32.7272))

    camUIImages['TEXT-WIND/UP/MUSICBOX']=pygame.transform.scale(sheet.image_at((1,693,142,37), colorkey =(90,90,90)), (WIDTH/7.804,HEIGHT/16.875))
    camUIImages['TEXT-CLICK&HOLD']=pygame.transform.scale(sheet.image_at((1,731,154,14), colorkey =(90,90,90)), (WIDTH/7.111,HEIGHT/43.2))
    camUIImages['TEXT-SIGNAL/INTERRUPTED']=pygame.transform.scale(sheet.image_at((1,746,340,22), colorkey =(90,90,90)), (WIDTH/5.647,HEIGHT/49.09))
    camUIImages['TEXT-EER']=pygame.transform.scale(sheet.image_at((342,755,43,13), colorkey =(90,90,90)), (WIDTH/44/651,HEIGHT/83.076))
    
    camUIImages['CAM-DOT']=pygame.transform.scale(sheet.image_at((373,445,44,43), colorkey =(5,5,5)), (WIDTH/27.428,HEIGHT/16.615))
    camUIImages['CAM-CAUTION_YELLOW']=pygame.transform.scale(sheet.image_at((296,356,57,49), colorkey =(5,5,5)), (WIDTH/33.684,HEIGHT/22.04))
    camUIImages['CAM-CAUTION_RED']=pygame.transform.scale(sheet.image_at((354,356,63,55), colorkey =(5,5,5)), (WIDTH/30.476,HEIGHT/19.636))
    camUIImages['CAM-MUSICBUTTON_GREY']=pygame.transform.scale(sheet.image_at((1,627,156,65), colorkey =(5,5,5)), (WIDTH/7.111,HEIGHT/9.818))
    camUIImages['CAM-MUSICBUTTON_GREEN']=pygame.transform.scale(sheet.image_at((158,627,156,65), colorkey =(5,5,5)), (WIDTH/7.111,HEIGHT/9.818))
    
    camUIImages['CAM-MUSIC_BAR1']=pygame.transform.scale(sheet.image_at((1,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR2']=pygame.transform.scale(sheet.image_at((56,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR4']=pygame.transform.scale(sheet.image_at((111,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR5']=pygame.transform.scale(sheet.image_at((166,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR6']=pygame.transform.scale(sheet.image_at((221,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR7']=pygame.transform.scale(sheet.image_at((276,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR7']=pygame.transform.scale(sheet.image_at((331,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR8']=pygame.transform.scale(sheet.image_at((386,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR9']=pygame.transform.scale(sheet.image_at((441,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR10']=pygame.transform.scale(sheet.image_at((496,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR11']=pygame.transform.scale(sheet.image_at((551,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR12']=pygame.transform.scale(sheet.image_at((606,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR13']=pygame.transform.scale(sheet.image_at((661,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR14']=pygame.transform.scale(sheet.image_at((716,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR15']=pygame.transform.scale(sheet.image_at((771,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR16']=pygame.transform.scale(sheet.image_at((826,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR17']=pygame.transform.scale(sheet.image_at((881,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR18']=pygame.transform.scale(sheet.image_at((936,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR19']=pygame.transform.scale(sheet.image_at((991,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR20']=pygame.transform.scale(sheet.image_at((1046,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    camUIImages['CAM-MUSIC_BAR21']=pygame.transform.scale(sheet.image_at((1101,770,54,54), colorkey =(5,5,5)), (WIDTH/17.614,HEIGHT/9.908))
    
def loadTitleScreen():
    global titleImages
    sheet=Spritesheet('titlescreen-SS.png')

    titleImages={}
    
def loadOverlays():
    global overlayImages
    sheet=Spritesheet('overlays-SS.png')
    
    overlayImages={}
    overlayImages['STATIC1']=pygame.transform.scale(sheet.image_at((1,770,1024,768)), (WIDTH,HEIGHT))
    overlayImages['STATIC2']=pygame.transform.scale(sheet.image_at((1026,770,1024,768)), (WIDTH,HEIGHT))
    overlayImages['STATIC3']=pygame.transform.scale(sheet.image_at((2051,770,1024,768)), (WIDTH,HEIGHT))
    overlayImages['STATIC4']=pygame.transform.scale(sheet.image_at((3076,770,1024,768)), (WIDTH,HEIGHT))
    overlayImages['STATIC5']=pygame.transform.scale(sheet.image_at((4101,770,1024,768)), (WIDTH,HEIGHT))
    overlayImages['STATIC6']=pygame.transform.scale(sheet.image_at((5126,770,1024,768)), (WIDTH,HEIGHT))
    
    overlayImages['WHITE1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    overlayImages['WHITE2']=pygame.transform.scale(sheet.image_at((1026,1,1024,768),colorkey =(10,10,0)), (WIDTH,HEIGHT))
    overlayImages['WHITE3']=pygame.transform.scale(sheet.image_at((2051,1,1024,768),colorkey =(10,10,0)), (WIDTH,HEIGHT))
    overlayImages['WHITE4']=pygame.transform.scale(sheet.image_at((3076,1,1024,768),colorkey =(10,10,0)), (WIDTH,HEIGHT))
    overlayImages['WHITE5']=pygame.transform.scale(sheet.image_at((4101,1,1024,768),colorkey =(10,10,0)), (WIDTH,HEIGHT))
    
def loadToyBonnie():
    global animatronicImages
    sheet=Spritesheet('ToyBonnie-SS.png')
    
    animatronicImages={}
    animatronicImages['ANIM-TB/OFFICE']=pygame.transform.scale(sheet.image_at((1026,4615,645,895), colorkey =(10,10,0)), (WIDTH/2.105,HEIGHT/.853))
    animatronicImages['ANIM-BLACKSCREEN']=pygame.transform.scale(sheet.image_at((1265,5168,1,1), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS2']=pygame.transform.scale(sheet.image_at((1,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS3']=pygame.transform.scale(sheet.image_at((1,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS4']=pygame.transform.scale(sheet.image_at((1,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS5']=pygame.transform.scale(sheet.image_at((1,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS6']=pygame.transform.scale(sheet.image_at((1,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS7']=pygame.transform.scale(sheet.image_at((1,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS8']=pygame.transform.scale(sheet.image_at((1026,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS9']=pygame.transform.scale(sheet.image_at((1026,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS10']=pygame.transform.scale(sheet.image_at((1026,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS11']=pygame.transform.scale(sheet.image_at((1026,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS12']=pygame.transform.scale(sheet.image_at((1026,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TB_JS13']=pygame.transform.scale(sheet.image_at((1026,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    
def loadToyChica():

    sheet=Spritesheet('ToyChica-SS.png')
    
    animatronicImages['ANIM-TC/OFFICE']=pygame.transform.scale(sheet.image_at((1026,4615,645,895), colorkey =(10,10,0)), (WIDTH/2.105,HEIGHT/.853))
    animatronicImages['ANIM-TC_JS1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS2']=pygame.transform.scale(sheet.image_at((1,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS3']=pygame.transform.scale(sheet.image_at((1,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS4']=pygame.transform.scale(sheet.image_at((1,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS5']=pygame.transform.scale(sheet.image_at((1,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS6']=pygame.transform.scale(sheet.image_at((1,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS7']=pygame.transform.scale(sheet.image_at((1,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS8']=pygame.transform.scale(sheet.image_at((1026,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS9']=pygame.transform.scale(sheet.image_at((1026,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS10']=pygame.transform.scale(sheet.image_at((1026,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS11']=pygame.transform.scale(sheet.image_at((1026,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS12']=pygame.transform.scale(sheet.image_at((1026,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TC_JS13']=pygame.transform.scale(sheet.image_at((1026,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))

def loadToyFreddy():
    
    sheet=Spritesheet('ToyFreddy-SS.png')
    
    animatronicImages['ANIM-TF/OFFICE']=pygame.transform.scale(sheet.image_at((1,4615,391,576), colorkey =(10,10,0)), (WIDTH/3.106,HEIGHT/1.146))
    animatronicImages['ANIM-TF_JS1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS2']=pygame.transform.scale(sheet.image_at((1,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS3']=pygame.transform.scale(sheet.image_at((1,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS4']=pygame.transform.scale(sheet.image_at((1,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS5']=pygame.transform.scale(sheet.image_at((1,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS6']=pygame.transform.scale(sheet.image_at((1,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS7']=pygame.transform.scale(sheet.image_at((1026,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS8']=pygame.transform.scale(sheet.image_at((1026,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS9']=pygame.transform.scale(sheet.image_at((1026,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS10']=pygame.transform.scale(sheet.image_at((1026,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS11']=pygame.transform.scale(sheet.image_at((1026,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-TF_JS12']=pygame.transform.scale(sheet.image_at((1026,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
def loadWitheredBonnie():
    sheet=Spritesheet('WitheredBonnie-SS.png')
    
    animatronicImages['ANIM-WB_JS1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS2']=pygame.transform.scale(sheet.image_at((1,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS3']=pygame.transform.scale(sheet.image_at((1,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS4']=pygame.transform.scale(sheet.image_at((1,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS5']=pygame.transform.scale(sheet.image_at((1,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS6']=pygame.transform.scale(sheet.image_at((1,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS7']=pygame.transform.scale(sheet.image_at((1,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS8']=pygame.transform.scale(sheet.image_at((1,5384,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS9']=pygame.transform.scale(sheet.image_at((1026,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS10']=pygame.transform.scale(sheet.image_at((1026,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS11']=pygame.transform.scale(sheet.image_at((1026,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS12']=pygame.transform.scale(sheet.image_at((1026,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS13']=pygame.transform.scale(sheet.image_at((1026,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS14']=pygame.transform.scale(sheet.image_at((1026,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS15']=pygame.transform.scale(sheet.image_at((1026,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WB_JS16']=pygame.transform.scale(sheet.image_at((1026,5384,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    
def loadWitheredChica():
    sheet=Spritesheet('WitheredChica-SS.png')
    
    animatronicImages['ANIM-WC_JS1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS2']=pygame.transform.scale(sheet.image_at((1,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS3']=pygame.transform.scale(sheet.image_at((1,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS4']=pygame.transform.scale(sheet.image_at((1,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS5']=pygame.transform.scale(sheet.image_at((1,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS6']=pygame.transform.scale(sheet.image_at((1,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS7']=pygame.transform.scale(sheet.image_at((1026,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS8']=pygame.transform.scale(sheet.image_at((1026,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS9']=pygame.transform.scale(sheet.image_at((1026,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS10']=pygame.transform.scale(sheet.image_at((1026,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS11']=pygame.transform.scale(sheet.image_at((1026,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WC_JS12']=pygame.transform.scale(sheet.image_at((1026,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
def loadWitheredFreddy():
    sheet=Spritesheet('WitheredFreddy-SS.png')
    
    animatronicImages['ANIM-WF_JS1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS2']=pygame.transform.scale(sheet.image_at((1,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS3']=pygame.transform.scale(sheet.image_at((1,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS4']=pygame.transform.scale(sheet.image_at((1,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS5']=pygame.transform.scale(sheet.image_at((1,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS6']=pygame.transform.scale(sheet.image_at((1,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS7']=pygame.transform.scale(sheet.image_at((1,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS8']=pygame.transform.scale(sheet.image_at((1026,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS9']=pygame.transform.scale(sheet.image_at((1026,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS10']=pygame.transform.scale(sheet.image_at((1026,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS11']=pygame.transform.scale(sheet.image_at((1026,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS12']=pygame.transform.scale(sheet.image_at((1026,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WF_JS13']=pygame.transform.scale(sheet.image_at((1026,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
def loadWitheredFoxy():
    sheet=Spritesheet('WitheredFoxy-SS.png')
    
    animatronicImages['ANIM-WFO_JS1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS2']=pygame.transform.scale(sheet.image_at((1,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS3']=pygame.transform.scale(sheet.image_at((1,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS4']=pygame.transform.scale(sheet.image_at((1,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS5']=pygame.transform.scale(sheet.image_at((1,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS6']=pygame.transform.scale(sheet.image_at((1,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS7']=pygame.transform.scale(sheet.image_at((1,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS8']=pygame.transform.scale(sheet.image_at((1026,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS9']=pygame.transform.scale(sheet.image_at((1026,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS10']=pygame.transform.scale(sheet.image_at((1026,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS11']=pygame.transform.scale(sheet.image_at((1026,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS12']=pygame.transform.scale(sheet.image_at((1026,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS13']=pygame.transform.scale(sheet.image_at((1026,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-WFO_JS14']=pygame.transform.scale(sheet.image_at((1026,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    
def loadMangle():
    sheet=Spritesheet('Mangle-SS.png')
    
    animatronicImages['MANGLE-PRISECOUNTER']=pygame.transform.scale(sheet.image_at((346,5,899,389), colorkey =(10,10,0)), (1271,550))
    animatronicImages['MANGLE-GAMEAREA']=pygame.transform.scale(sheet.image_at((347,403,606,398), colorkey =(10,10,0)), (857,563))
    animatronicImages['MANGLE-MAINHALL']=pygame.transform.scale(sheet.image_at((4,810,750,313), colorkey =(10,10,0)), (1061,443))
    animatronicImages['MANGLE-PARTYROOM2']=pygame.transform.scale(sheet.image_at((5,5,332,591), colorkey =(10,10,0)), (470,836))
    animatronicImages['MANGLE-OFFICE']=pygame.transform.scale(sheet.image_at((965,404,486,191), colorkey =(10,10,0)), (687,270))
def loadPuppet():
    sheet=Spritesheet('Puppet-SS.png')
    
    animatronicImages['ANIM-P_JS1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS2']=pygame.transform.scale(sheet.image_at((1,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS3']=pygame.transform.scale(sheet.image_at((1,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS4']=pygame.transform.scale(sheet.image_at((1,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS5']=pygame.transform.scale(sheet.image_at((1,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS6']=pygame.transform.scale(sheet.image_at((1,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS7']=pygame.transform.scale(sheet.image_at((1,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS8']=pygame.transform.scale(sheet.image_at((1,5384,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS9']=pygame.transform.scale(sheet.image_at((1026,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS10']=pygame.transform.scale(sheet.image_at((1026,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS11']=pygame.transform.scale(sheet.image_at((1026,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS12']=pygame.transform.scale(sheet.image_at((1026,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS13']=pygame.transform.scale(sheet.image_at((1026,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS14']=pygame.transform.scale(sheet.image_at((1026,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS15']=pygame.transform.scale(sheet.image_at((1026,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-P_JS16']=pygame.transform.scale(sheet.image_at((1026,5384,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
def loadGoldenFreddy():
    
    sheet=Spritesheet('GoldenFreddy-SS.png')
    
    animatronicImages['ANIM-GF/OFFICE']=pygame.transform.scale(sheet.image_at((1026,4615,379,379), colorkey =(10,10,0)), (700,700))
    animatronicImages['ANIM-GF_JS1']=pygame.transform.scale(sheet.image_at((1,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS2']=pygame.transform.scale(sheet.image_at((1,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS3']=pygame.transform.scale(sheet.image_at((1,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS4']=pygame.transform.scale(sheet.image_at((1,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS5']=pygame.transform.scale(sheet.image_at((1,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS6']=pygame.transform.scale(sheet.image_at((1,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS7']=pygame.transform.scale(sheet.image_at((1,4615,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS8']=pygame.transform.scale(sheet.image_at((1026,1,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS9']=pygame.transform.scale(sheet.image_at((1026,770,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS10']=pygame.transform.scale(sheet.image_at((1026,1539,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS11']=pygame.transform.scale(sheet.image_at((1026,2308,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS12']=pygame.transform.scale(sheet.image_at((1026,3077,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
    animatronicImages['ANIM-GF_JS13']=pygame.transform.scale(sheet.image_at((1026,3846,1024,768), colorkey =(10,10,0)), (WIDTH,HEIGHT))
def mainloop():
    running = True
    clock = pygame.time.Clock()
    while running:
        update()
        draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
            elif event.type == pygame.MOUSEMOTION:
                onMouseMove(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONDOWN:
                onMousePress(event.pos[0], event.pos[1])
            elif event.type == pygame.MOUSEBUTTONUP:
                onMouseRelease(event.pos[0], event.pos[1])
            elif event.type == pygame.KEYDOWN:
                onKeyPress(event.key)
            elif event.type == pygame.KEYUP:
                onKeyRelease(event.key)
        clock.tick(FPS)


pygame.init()
loadOffice()
loadOfficeInteractives()
loadCameraFrames()
loadOfficeDesk()
loadShowStageCam()
loadGameAreaCam()
loadkidsCoveCam()
loadPriseCornerCam()
loadMainHallCam()
loadPartyRoom1Cam()
loadPartyRoom2Cam()
loadPartyRoom3Cam()
loadPartyRoom4Cam()
loadPartsandServiceCam()
loadVentCams()
loadCamUI()
loadTitleScreen()
loadOverlays()
loadToyBonnie()
loadToyChica()
loadToyFreddy()
loadWitheredBonnie()
loadWitheredChica()
loadWitheredFreddy()
loadWitheredFoxy()
loadPuppet()
loadMangle()
loadGoldenFreddy()
setUpSFX()
setUpAnimatronics()
setupOfficeInts()
setupCams()
mainloop()

