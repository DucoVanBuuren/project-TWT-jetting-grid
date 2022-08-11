/**
 * @file    ProtocolManager.h
 * @author  Dennis van Gils (vangils.dennis@gmail.com)
 * @version https://github.com/Dennis-van-Gils/project-TWT-jetting-grid
 * @date    10-08-2022
 *
 * @brief   ...
 *
 * @section Abbrevations
 * - PCS: Protocol Coordinate System
 * - P  : Point in the PCS
 *
 * @copyright MIT License. See the LICENSE file for details.
 */

#ifndef PROTOCOL_MANAGER_H_
#define PROTOCOL_MANAGER_H_

#include "constants.h"
#include <Arduino.h>
#include <array>

// Common character buffer for string formatting, see `main.cpp`
extern const uint8_t BUF_LEN;
extern char buf[];

// TODO: descr
const uint16_t MAX_LINES = 5000;

// TODO: descr
const uint16_t MAX_POINTS_PER_LINE = NUMEL_PCS_AXIS * NUMEL_PCS_AXIS;

/*------------------------------------------------------------------------------
  P "Point in the Protocol Coordinate System (PCS)"
------------------------------------------------------------------------------*/

/**
 * @brief Special value denoting an uninitialized point in the PCS.
 */
const int8_t P_NULL_VAL = -128;

/**
 * @brief Class to hold and manage a single PCS point.
 */
class P {
public:
  P(int8_t x_ = P_NULL_VAL, int8_t y_ = P_NULL_VAL);

  inline bool isNull() const {
    return ((x == P_NULL_VAL) || (y == P_NULL_VAL));
  }

  inline void setNull() {
    x = P_NULL_VAL;
    y = P_NULL_VAL;
  }

  void print(Stream &mySerial);

  int8_t x;
  int8_t y;
};

/*------------------------------------------------------------------------------
  Structures and typedefs
------------------------------------------------------------------------------*/

/**
 * @brief TODO descr
 *
 * An `std::array` for elements of a class type calls their default constructor.
 * Hence, the default initialization here is an array full with special valued
 * `P` objects: `P{P_NULL_VAL, P_NULL_VAL`}.
 * See, https://cplusplus.com/reference/array/array/array/.
 */
using Line = std::array<P, MAX_POINTS_PER_LINE>;

/**
 * @brief TODO descr
 *
 * Is a bitmask, in essence, decoding all the active points of the PCS.
 * Benefit to packing is the constant array dimension and less memory footprint
 * than using `Line` when using a large number of points `P`.
 *
 * An `std::array` for elements of fundamental types are left uninitialized,
 * unless the array object has static storage, in which case they are zero-
 * initialized. Hence, the default initialization here is zero-initialized
 * only when declared non-local.
 * See, https://cplusplus.com/reference/array/array/array/.
 */
using PackedLine = std::array<uint16_t, NUMEL_PCS_AXIS>;

struct TimeLine {
  uint32_t time;
  Line line;
};

struct PackedTimeLine {
  uint32_t time;
  PackedLine packed;
};

using Program = std::array<PackedTimeLine, MAX_LINES>;

/*------------------------------------------------------------------------------
  ProtocolManager
------------------------------------------------------------------------------*/

/**
 * @brief
 *
 */
class ProtocolManager {
public:
  ProtocolManager();

  void clear();

  PackedLine pack_and_add(const Line &line);
  void pack_and_add2(const Line &line);

  /**
   * @brief
   *
   * Danger: The member `line_buffer` is valid as long as no other call to
   * `unpack4()` is made.
   *
   * @param packed
   */
  void unpack(const PackedLine &packed);

  /**
   * @brief
   *
   * Danger: The member `line_buffer` is valid as long as no other call to
   * `unpack4()` is made.
   */
  void unpack2();

  // For use with `unpack`, Extra spot added for end sentinel `P_NULL_VAL`
  std::array<P, MAX_POINTS_PER_LINE + 1> line_buffer;

private:
  Program program_;
  uint16_t N_program_lines_;
  uint16_t current_pos_;
};

#endif
