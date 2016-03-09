dem = {}


def switch_on(*values):
    def dem_func(f):
        dem.update((v, f) for v in values)
        return f

    return dem_func


@switch_on('RGGB')
def dem_RGGB():
    print "   case A"


bayer = 'RGGB'
dem[bayer]()

# @switch_on('RGGB')
# def demosaic_RGGB():
#     print "   case A"
#
#
# @switch_on('BGGR')
# def demosaic_BGGR():
#     print "   case B"
#
#
# @switch_on('GBRG')
# def demosaic_GBRG():
#     print "   case C"
#
#
# @switch_on('GRBG')
# def demosaic_GRBG():
#     print "   case D"


#
#
# case = {}
#
# def switch_on(*values):
#     def case_func(f):
#         case.update((v, f) for v in values)
#         return f
#     return case_func
#
# @switch_on(0, 3, 5)
# def case_a(): print "   case A"
#
# @switch_on(1,2,4)
# def case_b(): print "   case B"
#
# def default(): print "   default"
#
# for i in (0,2,3,5,22):
#     print "Case: %i" % i
#     try:
#         case[i]()
#     except KeyError:
#         default()
#
# def default(): print "   default"
