from Matrix import *

def sc_to_svg(sc, filename, pts, xsize, ysize):
    point_radius = 4
    stroke_width = 2
    poly_opacity = .25
    line_opacity = .75
    f = open(filename, "w")
    f.write(''.join(["<svg width=\"", str(xsize),
        "\" height=\"", str(ysize), "\">\n"]))
    for i in reversed(range(len(sc))):
        if len(sc.R[i]) == 0:
            p = pts[i]
            f.write(''.join(["\t<circle cx=\"", str(p[0]),
                "\" cy=\"", str(p[1]),
                "\" r=\"", str(point_radius),
                "\" stroke=\"green\" ",
                "stroke-width=\"", str(stroke_width),
                "\" fill=\"yellow\" />\n"]))
        elif len(sc.R[i]) == 2:
            p0 = pts[sc.R[i][0]]
            p1 = pts[sc.R[i][1]]
            f.write(''.join(["\t<line x1=\"", str(p0[0]),
                "\" y1=\"",  str(p0[1]),
                "\" x2=\"", str(p1[0]),
                "\" y2=\"", str(p1[1]),
                "\" style=\"stroke:rgb(0,0,255);",
                "stroke-width:", str(stroke_width),
                ";opacity:", str(line_opacity),
                "\" />\n"]))
        else:
            v = sc.get_vertices(i)
            polypts = []
            string = "\t<polygon points=\""
            for p in v:
                polypts.append(pts[p])
                string = ''.join([string,
                    str(pts[p][0]), ",",
                    str(pts[p][1]), " "])
            string = ''.join([string,
                "\" style=\"fill:mediumpurple;",
                "stroke:purple;",
                "stroke-width:0;",
                "opacity:", str(poly_opacity),
                "\" />\n"])
            f.write(string)
    f.write('</svg>')
    f.close()

