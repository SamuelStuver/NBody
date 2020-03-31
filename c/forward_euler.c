
// C program to demonstrate 
// drawing a circle using 
// OpenGL 
#include<stdio.h> 
#include<GL/glut.h> 
#include<math.h> 
#include<time.h> 
#define pi 3.142857 
#define xWindowWidth 500
#define yWindowWidth 500
#define dt 0.01


struct body {
    double position[3];
    double velocity[3];
    int mass;
};
  
// function to initialize 
void myInit (void) 
{ 
    // making background color black as first  
    // 3 arguments all are 0.0 
    glClearColor(0.0, 0.0, 0.0, 1.0); 
      
    // making picture color green (in RGB mode), as middle argument is 1.0 
    glColor3f(0.0, 1.0, 0.0); 
      
    // breadth of picture boundary is 1 pixel 
    glPointSize(1.0); 
    glMatrixMode(GL_PROJECTION);  
    glLoadIdentity(); 
      
    // setting window dimension in X- and Y- direction 
    gluOrtho2D(-xWindowWidth, xWindowWidth, -yWindowWidth, yWindowWidth); 
} 

void plotPoint(double coord[3]) {
    glVertex3i(coord[0], coord[1], coord[2]); 
}

struct body calcAccel(struct body b[]) {
    int nBodies = sizeof(*b)/sizeof(b[0]);
    for (int i=0; i < nBodies; i++){
        for (int j=0; j < nBodies; j++){
            double rx = (b[i].position[0] - b[j].position[0]);
            double ry = (b[i].position[1] - b[j].position[1]);
            double rz = (b[i].position[2] - b[j].position[2]);
            double r[3] = {rx, ry, rz};
            double r2 = ( rx*rx + ry*ry + rz*rz );
            // Calculate current acceleration
            double a[3];
            for (int k = 0; k < 3; k++) {
                a[k] = -r[k] / (r2 * sqrt(r2));
                b[i].position[k] += b[i].velocity[k] * dt;
                b[i].velocity[k] += a[k] * dt;
            }
        }
    }

    return *b;

}
  
void display (void)  
{ 
    glClear(GL_COLOR_BUFFER_BIT); 
    glBegin(GL_POINTS); 

    struct body bodyA = {
        {-100,0,0},
        {0, -1, 0},
        1
    };
    struct body bodyB = {
        {100,0,0},
        {0, 1, 0},
        1
    };

    struct body bodies[2] = {bodyA, bodyB}; 

    int len=2;
    for (int t=0; t<10; t += dt) {
        for (int i=0; i<len; i++) {
            plotPoint(bodies[i].position);
        }
        calcAccel(bodies);
    }
        
    // plotPoint(pointA);
    // plotPoint(pointB);
    glEnd(); 
    glFlush(); 
} 
  
int main (int argc, char** argv) 
{ 
    glutInit(&argc, argv); 
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB); 
      
    // giving window size in X- and Y- direction 
    glutInitWindowSize(xWindowWidth, yWindowWidth); 
    glutInitWindowPosition(0, 0); 
      
    // Giving name to window 
    glutCreateWindow("Circle Drawing"); 
    myInit(); 
      
    glutDisplayFunc(display); 
    glutMainLoop(); 
} 