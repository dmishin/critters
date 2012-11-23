#include "critters.hpp"
#define FOR_RANGE(type, var, start, end) for(type var=(start), __end=(end); var!=__end; ++var)

int set_critters_func( BinaryBlockFunction *func )
{
  FOR_RANGE( uint8, a00, 0, 2){
    FOR_RANGE( uint8, a01, 0, 2){
      FOR_RANGE( uint8, a10, 0, 2){
	FOR_RANGE( uint8, a11, 0, 2){
	  int x = a00 + (a01 << 1) + (a10 << 2) + (a11 << 3 );
	  int s = a00 + a01 + a10 + a11;
	  int y;
	  if (s==2){
	    y = x;
	  }else if(s==3){
	    y = 0xf ^ (a11 + (a10 << 1) + (a01 << 2) + (a00 << 3 ));
	  }else{
	    y = 0xf ^ x;
	  }
	  func->output[x] = y;
	}}}}
  return 0;
}

inline uint8 nonzero( uint8 x )
{
  return x ? 1 : 0;
}

inline void update_block( BinaryBlockFunction *func, uint8 &a00, uint8 &a01, uint8 &a10, uint8 &a11 )
{
  int x = a00 + (a01 << 1) + (a10 << 2) + (a11 << 3 );
  uint8 out = func->output[x];
  a00 = nonzero(out & 0x1);
  a01 = nonzero(out & 0x2);
  a10 = nonzero(out & 0x4);
  a11 = nonzero(out & 0x8);
}

int evaluate_even( BinaryBlockFunction *func, uint8 *field, int w, int h )
{
  if (w %2 != 0 || h %2 != 0)
    return 0;

  int offset;
  for( int y = 0; y < h; y += 2){
    offset = y * w;
    for( int x = 0; x < w; x += 2, offset += 2){
      update_block( func,
		      field[offset], field[offset+1],
		      field[offset+w], field[offset+w+1] );
    }
  }
  return 1;
}

inline int wrap( int x, int h ){
  if ( x >= h ) return x - h;
  return x;
}

int evaluate_odd( BinaryBlockFunction *func, uint8 *field, int w, int h )
{
  if (w %2 != 0 || h %2 != 0)
    return 0;

  int offset;
  for( int y = 1; y < h+1; y += 2){
    uint8 *row1 = field + (y           * w);
    uint8 *row2 = field + (wrap(y+1,h) * w);

    for( int x = 1; x < w+1; x += 2, offset += 2){
      int x2 = wrap(x+1, w);
      update_block( func,
		    row1[x], row1[x2],
		    row2[x], row2[x2] );
    }
  }
  return 1;
}
