cl__1 = 0.1;
Point(1) = {0, 0, 0, 0.1};
Point(2) = {1, 0, 0, 0.1};
Point(3) = {1, 1, 0, 0.1};
Point(4) = {0, 1, 0, 0.1};
Line(7) = {1, 2};
Line(8) = {2, 3};
Line(9) = {3, 4};
Line(10) = {4, 1};
Line Loop(16) = {7, 8, 9, 10};
Plane Surface(16) = {16};
//Recombine Surface {16};
