     West Nile Virus Outbreak Project Python Code
This code was created to provide users and observers a 
tool in order to provide a method which informs Boulder residents of 
spraying operations, or avoidance,
in their respective locations. The code initially provides a map of the 
Boulder area, as well as layers which contain wet land, 
lake and reservoir, mosquito larval site, OSMP property, and address information.
These layers are buffered to a degree set by the user, and then an intersect 
reveals the relationship between these layers. A spatial join further processes
necessary data, and allows for the creation of an "avoid points" summation. When 
properly written, this code can also set a spatial reference, apply a simple 
renderer to a specific layer, and run a definition query with which authorities can 
determine notification potentials. Technically, the code is supported by a configuration dictionary, which is defined by the programmer,
and a "yaml" file, which connects remote information to the project, describes the project location, and describes the data format. The final product is an interactive map creation that is exportable and printable.
