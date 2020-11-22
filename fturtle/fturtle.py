import turtle as t

def graphics_init(size):
    t.title("Game - Snake")
    # t.speed(0)
    t.tracer(0, 0)
    t.hideturtle()
    t.setup(width=size[0], height=size[1])

def coordonnees(case, pas):
    return case[1] * pas + CONFIGS.ZONE_PLAN_MINI[0], -case[0] * pas + CONFIGS.ZONE_PLAN_MAXI[1]

def tracer_carre(t, dimension):
    for i in range(4):
        t.forward(dimension)
        t.right(90)

def tracer_carreC(t, coinG, coinD):
    t.up()
    t.goto(coinG[0], coinG[1])
    t.down()
    t.goto(coinG[0], coinD[1])
    t.goto(coinD[0], coinD[1])
    t.goto(coinD[0], coinG[1])
    t.goto(coinG[0], coinG[1])

def tracer_case(t, case, couleur, pas, dl=0):
    # t.goto(-150, -150)
    x, y = coordonnees(case, pas)
    t.up()
    # t.goto(x+pas/2, y-pas/2)
    t.goto(x + dl, y - dl)
    t.down()
    t.color(couleur)
    t.begin_fill()
    tracer_carre(t, pas - 2 * dl)
    t.end_fill()

def newlayer():
    layer = t.Turtle()
    layer.hideturtle()
    return layer

