/*
CubicalRipser: C++ system for computation of Cubical persistence pairs
Copyright 2017-2018 Takeki Sudo and Kazushi Ahara.
CubicalRipser is free software: you can redistribute it and/or modify it under
the terms of the GNU Lesser General Public License as published by the
Free Software Foundation, either version 3 of the License, or (at your option)
any later version.

CubicalRipser is deeply depending on 'Ripser', software for Vietoris-Rips 
persitence pairs by Ulrich Bauer, 2015-2016.  We appreciate Ulrich very much.
We rearrange his codes of Ripser and add some new ideas for optimization on it 
and modify it for calculation of a Cubical filtration.

This part of CubicalRiper is a calculator of cubical persistence pairs for 
2 dimensional pixel data. The input data format conforms to that of DIPHA.
 See more descriptions in README.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more details.
You should have received a copy of the GNU Lesser General Public License along
with this program.  If not, see <http://www.gnu.org/licenses/>.
*/


#include <fstream>
#include <iostream>
#include <algorithm>
#include <queue>
#include <vector>
#include <unordered_map>
#include <string>
#include <cstdint>

#include "cubicalripser_2dim.h"

using namespace std;

CubicalRipser2D::CubicalRipser2D(){}
CubicalRipser2D::~CubicalRipser2D(){}

void CubicalRipser2D::print_usage_and_exit(int exit_code) {
	cerr << "Usage: "
	     << "CR2 "
	     << "[options] [input_filename]" << endl
	     << endl
	     << "Options:" << endl
	     << endl
	     << "  --help           print this screen" << endl
	     << "  --format         use the specified file format for the input. Options are:" << endl
	     << "                     dipha          (pixel data in DIPHA file format; default)" << endl
	     << "                     perseus        (pixel data in Perseus file format)" << endl
	     << "  --threshold <t>  compute cubical complexes up to birth time <t>" << endl
	     << "  --output         name of file that will contain the persistence diagram " << endl
	     << "  --print          print persistence pairs on your console" << endl
	     << endl;

	exit(exit_code);
}

CubicalRipser2D::CubicalRipser2D(const char* filename, string format, double threshold) : file(filename) {
	
	ifstream file_stream(file);
	if (filename && file_stream.fail()) {
		cerr << "ERROR! Couldn't open file " << filename << std::endl;
		exit(-1);
	}

	if (format == "DIPHA"){
		format_type = DIPHA;
	}
	
	if ((file != NULL) && (file[0] != '\0')){
		dcg = new DenseCubicalGrids(file, threshold, format_type);
	}
	
	thres = threshold;
	
}

CubicalRipser2D::CubicalRipser2D(std::vector<std::vector<double> > data, double threshold){
	//	Generate the array from file
	dcg = new DenseCubicalGrids(data, threshold);
	thres = threshold;
}

void CubicalRipser2D::ComputeBarcode(const char* filename, string output_filename, 
									 string format, double threshold, bool print){
		
		ifstream file_stream(filename);
		if (filename && file_stream.fail()) {
			cerr << "ERROR! Couldn't open file " << filename << std::endl;
			exit(-1);
		}

		writepairs.clear();
		
		if (format == "DIPHA"){
			format_type = DIPHA;
		}
		
		//	Generate the array from file
		dcg = new DenseCubicalGrids(filename, threshold, format_type);
		
		//	Set up columns to reduce
		ctr = new ColumnsToReduce(dcg);
			
		//	Initialize ComputePairs object
		cp = new ComputePairs(dcg, ctr, writepairs, print);
		cp->compute_pairs_main(); // dim0
		
		cp->assemble_columns_to_reduce();

		cp->compute_pairs_main(); // dim1
		

		//	Save barcode
		int64_t p = writepairs.size();
		for(int64_t i = 0; i < p; ++i){
			if (writepairs[i].getDimension() == 1 && writepairs[i].getDeath() == threshold+1){}
			else{
			std::vector<double> x = {double(writepairs[i].getDimension()),double(writepairs[i].getBirth()), double(writepairs[i].getDeath())};
			m_Barcode.push_back(x);
			}
		}
		
		ofstream writing_file;

		string extension = ".csv";
		if(equal(extension.rbegin(), extension.rend(), output_filename.rbegin()) == true){
			string outname = output_filename;
			writing_file.open(outname, ios::out);

			if(!writing_file.is_open()){
				cout << "ERROR! Open file for output failed! " << endl;
			}

				
			for(int64_t i = 0; i < p; ++i){
				if (writepairs[i].getDimension() == 1 && writepairs[i].getDeath() == threshold+1){}
				else{writing_file << writepairs[i].getDimension() << ",";

				writing_file << writepairs[i].getBirth() << ",";
				writing_file << writepairs[i].getDeath() << endl;
				}
			}
			writing_file.close();
		} else {

			writing_file.open(output_filename, ios::out | ios::binary);

			if(!writing_file.is_open()){
				cout << "ERROR! Open file for output failed! " << endl;
			}

			int64_t mn = 8067171840;
			writing_file.write((char *) &mn, sizeof( int64_t )); // magic number
			int64_t type = 2;
			writing_file.write((char *) &type, sizeof( int64_t )); // type number of PERSISTENCE_DIAGRAM
			int64_t p = writepairs.size();
			cout << "the number of pairs : " << p << endl;
			writing_file.write((char *) &p, sizeof( int64_t )); // number of points in the diagram p
			for(int64_t i = 0; i < p; ++i){
				if (writepairs[i].getDimension() == 1 && writepairs[i].getDeath() == threshold+1){}
				else{
				int64_t writedim = writepairs[i].getDimension();
				writing_file.write((char *) &writedim, sizeof( int64_t )); // dim

				double writebirth = writepairs[i].getBirth();
				writing_file.write((char *) &writebirth, sizeof( double )); // birth
				
				double writedeath = writepairs[i].getDeath();
				writing_file.write((char *) &writedeath, sizeof( double )); // death
				}
			}
			writing_file.close();
		}		
}

void CubicalRipser2D::ComputeBarcode(const char* filename, string format, double threshold, bool print){
	
		ifstream file_stream(filename);
		if (filename && file_stream.fail()) {
			cerr << "ERROR! Couldn't open file " << filename << std::endl;
			exit(-1);
		}

		writepairs.clear();

		if (format == "DIPHA"){
			format_type = DIPHA;
		}
		
		//	Generate the array from file
		dcg = new DenseCubicalGrids(filename, threshold, format_type);
		
		//	Set up columns to reduce
		ctr = new ColumnsToReduce(dcg);
			
		//	Initialize ComputePairs object
		cp = new ComputePairs(dcg, ctr, writepairs, print);
		cp->compute_pairs_main(); // dim0
		
		cp->assemble_columns_to_reduce();

		cp->compute_pairs_main(); // dim1
		

		//	Save barcode
		int64_t p = writepairs.size();
		for(int64_t i = 0; i < p; ++i){
			if (writepairs[i].getDimension() == 1 && writepairs[i].getDeath() == threshold+1){}
			else{
			std::vector<double> x = {double(writepairs[i].getDimension()),double(writepairs[i].getBirth()), double(writepairs[i].getDeath())};
			m_Barcode.push_back(x);
			}
		}
}


void CubicalRipser2D::ComputeBarcode(){		
	
		writepairs.clear();
		
		//	Set up columns to reduce
		ctr = new ColumnsToReduce(dcg);
			
		//	Initialize ComputePairs object
		cp = new ComputePairs(dcg, ctr, writepairs, false);
		cp->compute_pairs_main(); // dim0
		
		cp->assemble_columns_to_reduce();

		cp->compute_pairs_main(); // dim1
		

		//	Save barcode
		int64_t p = writepairs.size();
		for(int64_t i = 0; i < p; ++i){
			if (writepairs[i].getDimension() == 1 && writepairs[i].getDeath() == thres+1){}
			else{
			std::vector<double> x = {double(writepairs[i].getDimension()),double(writepairs[i].getBirth()), double(writepairs[i].getDeath())};
			m_Barcode.push_back(x);
			}
		}
}
