import GL,GL_VFX



 
win = GL.Display_init_(flags=GL.D_Scale)
 
p1 = GL_VFX.Particles.Rect(
    surf=win,
    draw_surf=win,
    rect=[-1,-1,1,1],
    shape_data=['c',20,[[200,10,240]]],
    circle_speed=2
)

while win.CEUF():
    p1.Set_position(GL.Open_mouse.GET_POSITION())
    p1.P()

    
    