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

int is_func_valid(BinaryBlockFunction *func)
{
  for( int x = 0; x < 16; ++x){
    bool found = false;
    for( int y = 0; y < 16; ++y ){
      if (func->output[y]==x) {
	found = true;
	break;
      }
    }
    if (! found) return 0;
  }
  return 1;
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

int evaluate_odd( BinaryBlockFunction *func, uint8 *field, int w, int h )
{
  if (w %2 != 0 || h %2 != 0)
    return 0;

  for( int y = 1; y < h-1; y += 2){
    uint8* row = field + (y*w);

    update_block( func,
		    row[0], row[w-1],
		    row[w], row[w+w-1] );

    for( int x = 1; x < w-1; x += 2){
      update_block(func,
		     row[x],   row[x+1],
		     row[x+w], row[x+w+1] );
    }
  }
  //top and bottom rows
  uint8* last_row = field + (w * (h-1) );
  uint8* first_row = field;
  for ( int x = 1; x < w - 1; x += 2 ){
    update_block( func,
		    last_row [x], last_row [x+1],
		    first_row[x], first_row[x+1] );
  }
  //corner
  update_block(func,
	       last_row[w-1], last_row[0],
	       first_row[w-1], first_row[0]);

  return 1;
}
