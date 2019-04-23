# optical fitting script

a1=1e-1; a2=1e-1; a3=1e-1; b1=1e-1; b2=1e-1; b3=1e-1; g1=1e-1	# initialize parameter(a1~b3[arcmin], g1[arcmin/degree])

d_el(x,y)=b1*cos(x*pi/180.)+b2*sin(x*pi/180.)+b3+g1*y						# fitting formula for delta El
d_az(x,y)=a1*sin(y*pi/180.)+a2+a3*cos(y*pi/180.)+b1*sin(x*pi/180.)*sin(y*pi/180.)-b2*cos(x*pi/180.)*sin(y*pi/180.)     # fitting formula for delta Az

fit d_el(x,y) "$0" using 1:2:(($$4-480./2.)*4.02/60):(1) via b1,b2,b3,g1
fit d_az(x,y) "$0" using 1:2:((-$$3+640./2.)*4.02/60):(1) via a1,a2,a3

#splot "$0" using 1:2:((-$$3+640./2.)*4.02/60)
#splot "$0" using 1:2:(($$4-480./2.)*4.02/60)
#splot "$0" using 1:2:(d_az(1,2))
#splot "$0" using 1:2:(d_el(1,2))

print "finish fitting.\n=======================================================================\n"
print "a1~a3,b1~b3,g1[arcsec]."
print "a1= ",(a1*60)
print "a2= ",(a2*60)
print "a3= ",(a3*60)
print "b1= ",(b1*60)
print "b2= ",(b2*60)
print "b3= ",(b3*60)
print "g1= ",(g1*60)
print "\n"
print "a1~a3,b1~b3,g1[arcmin]."
print "a1= ",(a1)
print "a2= ",(a2)
print "a3= ",(a3)
print "b1= ",(b1)
print "b2= ",(b2)
print "b3= ",(b3)
print "g1= ",(g1)

