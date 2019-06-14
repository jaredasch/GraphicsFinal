import mdlA
from display import *
from matrix import *
from draw import *

def run(filename):
    """
    This function runs an mdl script
    """
    p = mdl.parseFile(filename)
    if p:
        (commands, symbols) = p
    else:
        print( "Parsing failed.")
        return

    view = [0,
            0,
            1];
    ambient = [50,
               50,
               50]
    light = [[0.5,
              0.75,
              1],
             [255,
              255,
              255]]

    color = [0, 0, 0]
    tmp = new_matrix()
    ident( tmp )

    stack = [ [x[:] for x in tmp] ]
    print(stack)
    screen = new_screen()
    zbuffer = new_zbuffer()
    tmp = []
    step_3d = 200
    consts = ''
    coords = []
    coords1 = []
    print(type(symbols))
    symbols['.white'] = ['constants',
                         {'red': [0.2, 0.5, 0.5],
                          'green': [0.2, 0.5, 0.5],
                          'blue': [0.2, 0.5, 0.5]}]
    reflect = '.white'
    polygons = []
    edges = []
    
    # print( symbols)
    #
    # print(commands)

    for command in commands:
        
        
        o = command['op']

        if o == 'mesh':
            filename = command["args"][0] + ".obj"
            load_mesh(tmp, filename)
            matrix_mult(stack[-1], tmp)
            draw_polygons(tmp, screen, zbuffer, view, ambient, light, symbols, reflect)
            tmp = []


        elif o == "save_coord_system":
            symbols[command["cs"]] = [i[:] for i in stack[-1]]
            
        elif o == "push":            
            stack.append([i[:] for i in stack[-1]])

        elif o == "pop":
            print(stack)
            print(stack.pop())

        elif o == "move":
            if len(command["args"]) == 1:
                a = command["args"][0]
                M = make_translate(symbols[a])
            else:  
                M = make_translate(* command["args"])
            matrix_mult(stack[-1], M)
            stack[-1] = [i[:] for i in M]

        elif o == "scale":
            M = make_scale(* command["args"])
            matrix_mult(stack[-1], M)
            stack[-1] = [i[:] for i in M]

        elif o == "rotate":
            #print command
            M = new_matrix()
            degrees = command["args"][1] * (math.pi / 180)
            if command["args"][0] == "x":
                M = make_rotX(degrees)
            elif command["args"][0] == "y":
                M = make_rotY(degrees)
            elif command["args"][0] == "z":
                M = make_rotZ(degrees)
            else:
                print("Not valid argument for rotation")
            matrix_mult(stack[-1], M)
            stack[-1] = [i[:] for i in M]

        elif o == "sphere":
            if command["cs"]:
                mult = symbols[command["cs"]]
                #print("used")
            else:
                mult = stack[-1]
                #print("default")
            args = [float(i) for i in command["args"][:4]]
            add_sphere(*[polygons]+ args +[ step_3d])
            #mult = stack[-1]
            matrix_mult(mult, polygons)
            
            if(command['constants']):
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif o == "torus":
            #print(command)
            if command["cs"]:

                mult = symbols[command["cs"]]
            else:
                mult = stack[-1]
            #print ("here is m")
            #print(mult)
            args = [float(i) for i in command["args"][:5]]
            add_torus(*[polygons] + args + [step_3d])
            #mult = stack[-1]
            matrix_mult(mult, polygons)
            if(command['constants']):
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif o == "box":
            #print(command)
            if command["cs"]:
                mult = symbols[command["cs"]]
            else:
                mult = stack[-1]
            args = [float(i) for i in command["args"][:6]]
            add_box(*[polygons] + args )            
            matrix_mult(mult, polygons)
            if(command['constants']):
                print(command["constants"])
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, command['constants'])
            else:
                draw_polygons(polygons, screen, zbuffer, view, ambient, light, symbols, reflect)
            polygons = []

        elif o == 'line':
            print(command)
            if command["cs0"]:
                cs0 = symbols[command["cs0"]]
            else:
                cs0 = stack[-1]
            if command["cs1"]:
                cs1 = symbols[command["cs1"]]
            else:
                cs1 = stack[-1]

            args = [float(i) for i in command["args"]]            
            add_edge(* [edges] + args)
            matrix_mult( cs0, [edges[0]] )
            matrix_mult( cs1, [edges[1]] )
            draw_lines(edges, screen, zbuffer, color)
            edges = []

        elif o == 'save':
            save_extension(screen, command["args"][0] + ".png")

        elif o == 'display':
            display(screen)

        elif o == "constants":
            pass
                        
        else:
            print("Try again")
        
        
                   
                
                


#run("face.mdl")
