//------------------------------------------------------------------------------------------------------------------------
//forward_euler1 -- from artcompsci.org (http://www.artcompsci.org/msa/web/vol_1/v1_web/node27.html)
//------------------------------------------------------------------------------------------------------------------------

#include <iostream>
#include <cmath>
using namespace std;

int main()
{
	double r[3], v[3], a[3];
	double dt = 0.01;

	// Initial position
	r[0] = 1;
	r[1] = 0;
	r[2] = 0;

	// Initial velocity
	v[0] = 0;
	v[1] = 0.5;
	v[2] = 0;

	for (int ns = 0; ns < 1000; ns++) {
		double r2 = (r[0] * r[0]) + (r[1] * r[1]) + (r[2] * r[2]);
		// Calculate current acceleration
		for (int k = 0; k < 3; k++) {
			a[k] = -r[k] / (r2 * sqrt(r2));
		}
		// Calcuate new position and velocity based on calculated acceleration
		for (int k = 0; k < 3; k++) {
			r[k] += v[k] * dt;
			v[k] += a[k] * dt;
		}

		cout << r[0] << " " << r[1] << " " << r[2] << " ";
		cout << v[0] << " " << v[1] << " " << v[2] << endl;
	}
}
