

#include <iostream>
#include <json/writer.h>
#include <cstdlib> //Unnecessary in real version?
//#include <random> //Unnecessary in real version
#include <fstream>
#include <unistd.h> //For Sleep(). Unnecessary in real version.

//for output filename stuff
#include <iomanip>
#include <sstream>


int main(){

    Json::Value data;

    srand (time(NULL));

    std::ofstream out_stream;

    for(int year=0; year<100; year++){
    for(int month=0; month<12; month++){

        data["Year"] = year;
        data["Month"] = month;
   
        //Monthly Thermal information 
        data["TempAir"] = rand()%100*1.0;
        data["TempOrganicLayer"] = rand()%100*1.0;
        data["TempMineralLayer"] = rand()%100*1.0;
        data["PAR"] = rand()%100*1.0;
        data["ActiveLayerDepth"] = rand()%100*1.0;

        //Monthly Hydrodynamic information
        data["Precipitation"] = rand()%100*1.0;
        data["WaterTable"] = rand()%100*1.0;
        data["VWCOrganicLayer"] = rand()%100*1.0;
        data["VWCMineralLayer"] = rand()%100*1.0;
        data["Evapotranspiration"] = rand()%100*1.0;


        //std::cout << data << std::endl;
        std::cout << "year: "<<year<<", month: "<<month<<std::endl;

        std::stringstream filename;
        filename.fill('0');
        filename << "tmp-json/" << std::setw(4) << year << "_" << std::setw(2) << month << ".json";

        out_stream.open(filename.str().c_str(), std::ofstream::out);

        out_stream << data << std::endl;

        out_stream.close();

        usleep(5000);
    }
    }

    std::cout<<std::endl;

    return 0;
}
