import numpy as np

# 2D Transformations

def reflect2D(verticies, param):
    if param == "x":
        tfMat = np.array([
                [1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
        ])
    elif param == 'y':
        tfMat = np.array([
                [-1, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
        ])
    elif param == 'y=x':
        tfMat = np.array([
                [0, 1, 0],
                [1, 0, 0],
                [0, 0, 1]
        ])
    elif param == 'y=-x':
        tfMat = np.array([
                [0, -1, 0],
                [-1, 0, 0],
                [0, 0, 1]
        ])
    else:
        temp = param.split(',')
        a = float(temp[0][1:])
        b = float(temp[1][:-1])
        translateToZeroMat = np.array([
                [1, 0, -a],
                [0, 1, -b],
                [0, 0, 1]
        ])
        reflectOriginMat = np.array([
                [-1, 0, 0],
                [0, -1, 0],
                [0, 0, 1]
        ])
        translateFromZeroMat = np.array([
                [1, 0, a],
                [0, 1, b],
                [0, 0, 1]
        ])
        tfMat = np.matmul(translateFromZeroMat, np.matmul(reflectOriginMat, translateToZeroMat)) 
    return Transform2D(verticies, tfMat)


def shear2D(verticies, param, k):
    if param == 'x':
        tfMat = np.array([
                [1, k, 0],
                [0, 1, 0],
                [0, 0, 1]
        ])
    elif param == 'y':
        tfMat = np.array([
                [1, 0, 0],
                [k, 1, 0],
                [0, 0, 1]
        ])
    return Transform2D(verticies, tfMat)


def custom2D(verticies, a, b, c, d):
    tfMat = np.array([
            [a, b, 0],
            [c, d, 0],
            [0, 0, 1]
    ])
    return Transform2D(verticies, tfMat)


def stretch2D(verticies, param, k):
    if param == 'x':
        tfMat = np.array([
                [k, 0, 0],
                [0, 1, 0],
                [0, 0, 1]
        ])
    elif param == 'y':
        tfMat = np.array([
                [1, 0, 0],
                [0, k, 0],
                [0, 0, 1]
        ])
    return Transform2D(verticies, tfMat)


def translate2D(verticies, dx, dy):
    tfMat = np.array([
            [1, 0, dx],
            [0, 1, dy],
            [0, 0, 1]
    ])
    return Transform2D(verticies, tfMat)


def dilate2D(verticies, k):
    tfMat = np.array([
            [k, 0, 0],
            [0, k, 0],
            [0, 0, 1]
    ])
    return Transform2D(verticies, tfMat)


def rotate2D(verticies, degree, x, y):
    translateToZeroMat = np.array([
            [1, 0, -x],
            [0, 1, -y],
            [0, 0, 1]
    ])
    RotateMat = np.array([
            [np.math.cos((degree/360)*2*np.pi), -
                         (np.math.sin((degree/360)*2*np.pi)), 0],
            [np.math.sin((degree/360)*2*np.pi),
                         np.math.cos((degree/360)*2*np.pi), 0],
            [0, 0, 1]
    ])
    translateBackMat = np.array([
            [1, 0, x],
            [0, 1, y],
            [0, 0, 1]
    ])
    tfMat = np.matmul(translateBackMat, np.matmul(
        RotateMat, translateToZeroMat))
    return Transform2D(verticies, tfMat)

def Transform2D(verticies, tfMat):
    newV = np.empty((0, 2), float)
    for vertex in verticies:
        vertex = np.append(vertex, [1])
        temp = np.matmul(tfMat, vertex.T)
        keep = [True, True, False]
        temp = np.array(temp[keep])
        temp = np.array([temp])
        newV = np.vstack((newV, temp))
    return newV

# 3D Transformations

def shear3D(verticies, param1, param2, k):
    if param1 == 'x':
        if param2 == 'y':
            tfMat = np.array([
                [1, k,0,0],
                [0, 1,0,0],
                [0, 0,1,0],
                [0, 0,0,1]
            ])
        elif param2 == 'z':
            tfMat = np.array([
                [1, 0,k,0],
                [0, 1,0,0],
                [0, 0,1,0],
                [0, 0,0,1]
            ])
    elif param1 == 'y':
        if param2 == 'x':
            tfMat = np.array([
                [1, 0,0,0],
                [k, 1,0,0],
                [0, 0,1,0],
                [0, 0,0,1]
            ])
        elif param2 == 'z':
            tfMat = np.array([
                [1, 0,0,0],
                [0, 1,k,0],
                [0, 0,1,0],
                [0, 0,0,1]
            ])
    elif param1 == 'z':
        if param2 == 'x':
            tfMat = np.array([
                [1, 0,0,0],
                [0, 1,0,0],
                [k, 0,1,0],
                [0, 0,0,1]
            ])
        elif param2 == 'y':
            tfMat = np.array([
                [1, 0,0,0],
                [0, 1,0,0],
                [0, k,1,0],
                [0, 0,0,1]
            ])
    return Transform3D(verticies, tfMat)


def custom3D(verticies, a, b, c, d, e, f, g, h, i):
    tfMat = np.array([
        [a, b,c,0],
        [d, e,f,0],
        [g, h,i,0],
        [0, 0,0,1]
    ])
    return Transform3D(verticies, tfMat)


def stretch3D(verticies, param, k):
    if param == 'x':
        tfMat = np.array([
            [k, 0,0,0],
            [0, 1,0,0],
            [0, 0,1,0],
            [0, 0,0,1]
        ])
    elif param == 'y':
        tfMat = np.array([
            [1, 0,0,0],
            [0, k,0,0],
            [0, 0,1,0],
            [0, 0,0,1]
        ])
    elif param == 'z':
        tfMat = np.array([
            [1, 0,0,0],
            [0, 1,0,0],
            [0, 0,k,0],
            [0, 0,0,1]
        ])
    return Transform3D(verticies, tfMat)


def translate3D(verticies, dx, dy, dz):
    tfMat = np.array([
        [1, 0,0,dx],
        [0, 1,0,dy],
        [0, 0,1,dz],
        [0, 0,0,1]
    ])
    return Transform3D(verticies, tfMat)


def dilate3D(verticies, k):
    tfMat = np.array([
        [k, 0,0,0],
        [0, k,0,0],
        [0, 0,k,0],
        [0, 0,0,1]
    ])
    return Transform3D(verticies, tfMat)


def reflect3D(verticies, param) :
    if param == "x":
        tfMat = np.array([
            [1, 0,0,0],
            [0, -1,0,0],
            [0, 0,-1,0],
            [0, 0,0,1]
        ])
    elif param == 'y':
        tfMat = np.array([
            [-1, 0,0,0],
            [0, 1,0,0],
            [0, 0,-1,0],
            [0, 0,0,1]
        ])
    elif param == 'z':
        tfMat = np.array([
            [-1, 0,0,0],
            [0, -1,0,0],
            [0, 0,1,0],
            [0, 0,0,1]
        ])
    elif param == 'xy':
        tfMat = np.array([
            [1, 0,0,0],
            [0, 1,0,0],
            [0, 0,-1,0],
            [0, 0,0,1]
        ])
    elif param == 'xz':
        tfMat = np.array([
            [1, 0,0,0],
            [0, -1,0,0],
            [0, 0,1,0],
            [0, 0,0,1]
        ])
    elif param == 'yz':
        tfMat = np.array([
            [-1, 0,0,0],
            [0, 1,0,0],
            [0, 0,1,0],
            [0, 0,0,1]
        ])
    elif param[0] == '(':
        temp = param.split(',')
        a = float(temp[0][1:])
        b = float(temp[1])
        c = float(temp[2][:-1])
        translateToZeroMat = np.array([
            [1, 0,0,-a],
            [0, 1,0,-b],
            [0, 0,1,-c],
            [0, 0,0,1]
        ])
        reflectOriginMat = np.array([
            [-1, 0,0,0],
            [0, -1,0,0],
            [0, 0,-1,0],
            [0, 0,0,1]
        ])
        translateFromZeroMat = np.array([
            [1, 0,0,a],
            [0, 1,0,b],
            [0, 0,1,c],
            [0, 0,0,1]
        ])
        tfMat = np.matmul(translateFromZeroMat, np.matmul(reflectOriginMat, translateToZeroMat))
    else:
        temp = param.split(',')
        a = float(temp[0])
        b = float(temp[1])
        c = float(temp[2])
        panjangVektor = np.sqrt(a*a+b*b+c*c)
        a /= panjangVektor
        b /= panjangVektor
        c /= panjangVektor
        ab = a*b
        ac = a*c
        bc = b*c
        tfMat = np.array([
            [1-(2*a*a), -2*ab,-2*ac,0],
            [-2*ab, 1-(2*b*b),-2*bc,0],
            [-2*ac, -2*bc,1-(2*c*c),0],
            [0, 0,0,1]
        ])
    return Transform3D(verticies, tfMat)


def rotate3D(verticies, a, b, c, degree) :
    panjangVektor = np.sqrt(a*a+b*b+c*c)
    a /= panjangVektor
    b /= panjangVektor
    c /= panjangVektor
    degree = degree*np.pi/180
    cosa = np.math.cos(degree)
    sina = np.math.sin(degree)
    ab = a*b
    bc = b*c
    ac = a*c
    tfMat = np.array([
        [cosa+((a**2)*(1-cosa)), ab*(1-cosa)-(c*sina),ac*(1-cosa)+(b*sina),0],
        [ab*(1-cosa)+(c*sina), cosa+((b**2)*(1-cosa)),bc*(1-cosa)-(a*sina),0],
        [ac*(1-cosa)-(b*sina), bc*(1-cosa)+(a*sina),cosa+((c**2)*(1-cosa)),0],
        [0, 0,0,1]
    ])
    return Transform3D(verticies, tfMat)


def Transform3D(verticies, tfMat):
    newV = np.empty((0, 3), float)
    for vertex in verticies:
        vertex = np.append(vertex, [1])
        temp = np.matmul(tfMat, vertex.T)
        keep = [True, True,True,False]
        temp = np.array(temp[keep])
        temp = np.array([temp])
        newV = np.vstack((newV, temp))
    return newV
