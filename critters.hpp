#ifndef __CRITTERS_HPP_INCLUDED__
#define __CRITTERS_HPP_INCLUDED__

#ifdef WIN32
#define CRITTERS_EXPORT __declspec(dllexport)
#else
#define CRITTERS_EXPORT 
#endif

typedef unsigned char uint8;
struct BinaryBlockFunction{
  uint8 output[16];
};
  

extern "C" {
  int CRITTERS_EXPORT set_critters_func( BinaryBlockFunction *func );
  int CRITTERS_EXPORT evaluate_even( BinaryBlockFunction *func, uint8 *field, int w, int h );
  int CRITTERS_EXPORT evaluate_odd( BinaryBlockFunction *func, uint8 *field, int w, int h );
}

#endif
