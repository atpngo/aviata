/*
* This file is automatically generated by px_generate_mixers.py - do not edit.
*/

#ifndef _AVIATA_MIXER_MULTI_TABLES
#define _AVIATA_MIXER_MULTI_TABLES

#define AVIATA_NUM_DRONES 2
#define AVIATA_NUM_ROTORS 6
#define AVIATA_MAX_MISSING_DRONES 0

static constexpr float _config_aviata_drone_angle[] {
	 0.000000, // 0.0 degrees
	 0.000000, // 0.0 degrees
};

enum class AviataMultirotorGeometry : MultirotorGeometryUnderlyingType {
	AVIATA_MISSING_,               // AVIATA with these drones missing:  (text key aviata_missing_)

	MAX_GEOMETRY
}; // enum class AviataMultirotorGeometry

namespace {
static constexpr MultirotorMixer::Rotor _config_aviata_aviata_missing_[] {
	{ -0.284915,  0.000000, -1.000000,  1.000000 },
	{ -0.284915,  0.000000,  1.000000,  1.000000 },
	{ -0.284915,  0.866025, -1.000000,  1.000000 },
	{ -0.284915, -0.866025,  1.000000,  1.000000 },
	{ -0.284915,  0.866025,  1.000000,  1.000000 },
	{ -0.284915, -0.866025, -1.000000,  1.000000 },
	{  0.284915,  0.000000, -1.000000,  1.000000 },
	{  0.284915,  0.000000,  1.000000,  1.000000 },
	{  0.284915,  0.866025, -1.000000,  1.000000 },
	{  0.284915, -0.866025,  1.000000,  1.000000 },
	{  0.284915,  0.866025,  1.000000,  1.000000 },
	{  0.284915, -0.866025, -1.000000,  1.000000 },
};

static constexpr const MultirotorMixer::Rotor *_config_aviata_index[] {
	&_config_aviata_aviata_missing_[0],
};

static constexpr unsigned _config_aviata_rotor_count[] {
	12, /* aviata_missing_ */
};

const char* _config_aviata_key[] {
	"aviata_missing_",	/* aviata_missing_ */
};

} // anonymous namespace

#endif /* _AVIATA_MIXER_MULTI_TABLES */
