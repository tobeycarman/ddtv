

#include <iostream>
#include <json/writer.h>
#include <cstdlib> //Unnecessary in real version?
#include <random> //Unnecessary in real version
#include <fstream>
#include <unistd.h> //For Sleep(). Unnecessary in real version.


int main(){

    Json::Value data;

    srand (time(NULL));

    std::ofstream out_stream("output.json", std::ofstream::out);

    for(int ii=0; ii<200; ii++){
   
        //Monthly Thermal information 
        data["TempAir"] = rand()%100;
        data["TempOrganicLayer"] = rand()%100;
        data["TempMineralLayer"] = rand()%100;
        data["PAR"] = rand()%100;
        data["ActiveLayerDepth"] = rand()%100;

        //Monthly Hydrodynamic information
        //etc...

        //std::cout << data << std::endl;
        std::cout << ii << " " << std::endl;

        out_stream << data << std::endl;
        out_stream.seekp(std::ios::beg);

        sleep(1);
    }

    std::cout<<std::endl;

    out_stream.close();

    return 0;
}
