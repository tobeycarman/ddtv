

#include <iostream>
#include <json/writer.h>
#include <cstdlib> //Unnecessary in real version?
//#include <random> //Unnecessary in real version
#include <fstream>
#include <unistd.h> //For Sleep(). Unnecessary in real version.
#include <cmath>//for sin(). Unnecessary...

//for output filename stuff
#include <iomanip>
#include <sstream>
#include <cstring> //for strcmp()

int main(int argc, char *argv[]) {

    int YRS = 100;
    int DELAY = 1000; // micro secs? 1,000,000 per second

    if (argc >= 3) {
      if ( ((argc-1) % 2) != 0 ) {
        std::cerr << "Wrong number of arguments!\n";
        exit(-1);
      }
      for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "-y") == 0) {
          std::stringstream v( argv[i+1] );
          if ( !(v >> YRS) ) {
            std::cerr << "Error converting arg...\n";
          }
        }

        if (strcmp(argv[i], "-d") == 0) {
          std::stringstream v( argv[i+1] );
          if ( !(v >> DELAY) ) {
            std::cerr << "Error converting arg...\n";
          }
        }
      }
    }

    Json::Value data;

    srand (time(NULL));

    std::ofstream out_stream;

    for(int year=0; year<YRS; year++){
    for(int month=0; month<12; month++){

        data["Year"] = year;
        data["Month"] = month;
   
        //Monthly Thermal information 
        data["TempAir"] = sin((month/2.))*100;
        data["TempOrganicLayer"] = 75.0;
        data["TempMineralLayer"] = rand()%100*1.0;
        data["PAR"] = rand()%100*1.0;
        data["ActiveLayerDepth"] = rand()%100*1.0;

        //Monthly Hydrodynamic information
        data["Precipitation"] = rand()%100*1.0;
        data["WaterTable"] = sin((month/2.))*100;
        data["VWCOrganicLayer"] = rand()%100*1.0;
        data["VWCMineralLayer"] = rand()%100*1.0;
        data["Evapotranspiration"] = rand()%100*1.0;


        //std::cout << data << std::endl;
        std::cout << "year: "<<year<<", month: "<<month<<std::endl;

        std::stringstream filename;
        filename.fill('0');
        //filename << "tmp-json/" << std::setw(4) << year << "_" << std::setw(2) << month << ".json";
        filename << "/tmp/cal-dvmdostem/" << std::setw(4) << year << "_" << std::setw(2) << month << ".json";

        out_stream.open(filename.str().c_str(), std::ofstream::out);

        out_stream << data << std::endl;

        out_stream.close();

        usleep(DELAY);
    }
    }

    std::cout<<std::endl;

    return 0;
}
