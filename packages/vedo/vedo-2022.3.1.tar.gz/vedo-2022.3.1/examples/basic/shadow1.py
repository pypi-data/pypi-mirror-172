"""Cast a shadow of 2 meshes onto the wall"""
from vedo import dataurl, Mesh, Sphere, show

spider = Mesh(dataurl+"spider.ply")
spider.texture(dataurl+'textures/leather.jpg')

spider.normalize().rotateZ(-90).addShadow('x', -3, alpha=0.5)

sphere = Sphere(r=0.3).pos(0.4,0,0.6).addShadow('x', -3)

show(spider, sphere, __doc__, axes=1, viewup="z").close()
