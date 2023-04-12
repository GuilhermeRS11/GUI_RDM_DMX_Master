"""
#****************************************************************/
# Entertainment Services Technology Association (ESTA)          */
# ANSI E1.20 Remote Device Management (RDM) over DMX512 Networks*/
#****************************************************************/
#                                                               */
#                          RDM.h                                */
#                                                               */
#****************************************************************/
# Appendix A Defines for the RDM Protocol.                      */
# Publish date: 3/31/2006                                       */
#****************************************************************/
# Compiled by: Scott M. Blair   8/18/2006                       */
# Updated 10/11/2011: Adding E1.20-2010 and E1.37-1 defines.    */
# Updated 10/24/2014: Adding E1.37-2 defines                    */
#****************************************************************/
# For updates see: http:#www.rdmprotocol.org                   */
#****************************************************************/
# Copyright 2006,2011, 2014 Litespeed Design                    */
#****************************************************************/
# Permission to use, copy, modify, and distribute this software */
# is freely granted, provided that this notice is preserved.    */
#****************************************************************/
"""
# Protocol version. */
E120_PROTOCOL_VERSION  = 0x0100

# RDM START CODE (Slot 0)                                                                                                     */
E120_SC_RDM = 0xCC

# RDM Protocol Data Structure ID's (Slot 1)                                                                                   */
E120_SC_SUB_MESSAGE = 0x01

# Broadcast Device UID's                                                                                                      */
E120_BROADCAST_ALL_DEVICES_ID = 0xFFFFFFFFFFFF   # (Broadcast all Manufacturers)                    */
# ALL_DEVICES_ID                                  0xmmmmFFFFFFFF   # (Specific Manufacturer ID 0xmmmm)                */

E120_SUB_DEVICE_ALL_CALL = 0xFFFF


#*******************************************************/
# Table A-1: RDM Command Classes (Slot 20)             */
#*******************************************************/
E120_DISCOVERY_COMMAND = 0x10
E120_DISCOVERY_COMMAND_RESPONSE = 0x11
E120_GET_COMMAND = 0x20
E120_GET_COMMAND_RESPONSE = 0x21
E120_SET_COMMAND = 0x30
E120_SET_COMMAND_RESPONSE = 0x31



#*******************************************************/
# Table A-2: RDM Response Type (Slot 16)               */
#*******************************************************/
E120_RESPONSE_TYPE_ACK = 0x00
E120_RESPONSE_TYPE_ACK_TIMER = 0x01
E120_RESPONSE_TYPE_NACK_REASON = 0x02   # See Table A-17                                              */
E120_RESPONSE_TYPE_ACK_OVERFLOW = 0x03   # Additional Response Data available beyond single response length.*/


#*******************************************************/
# Table A-3: RDM Parameter ID's (Slots 21-22)          */
#*******************************************************/
# Category - Network Management   */
E120_DISC_UNIQUE_BRANCH = 0x0001
E120_DISC_MUTE = 0x0002
E120_DISC_UN_MUTE = 0x0003
E120_PROXIED_DEVICES = 0x0010
E120_PROXIED_DEVICE_COUNT = 0x0011
E120_COMMS_STATUS = 0x0015

# Category - Status Collection    */
E120_QUEUED_MESSAGE = 0x0020 # See Table A-4                                              */
E120_STATUS_MESSAGES = 0x0030 # See Table A-4                                              */
E120_STATUS_ID_DESCRIPTION = 0x0031
E120_CLEAR_STATUS_ID = 0x0032
E120_SUB_DEVICE_STATUS_REPORT_THRESHOLD = 0x0033 # See Table A-4                                              */

# Category - RDM Information      */
E120_SUPPORTED_PARAMETERS = 0x0050 # Support required only if supporting Parameters beyond the minimum required set.*/
E120_PARAMETER_DESCRIPTION = 0x0051 # Support required for Manufacturer-Specific PIDs exposed in SUPPORTED_PARAMETERS message */
# Category - Product Information  */
E120_DEVICE_INFO = 0x0060
E120_PRODUCT_DETAIL_ID_LIST = 0x0070
E120_DEVICE_MODEL_DESCRIPTION = 0x0080
E120_MANUFACTURER_LABEL = 0x0081
E120_DEVICE_LABEL = 0x0082
E120_FACTORY_DEFAULTS = 0x0090
E120_LANGUAGE_CAPABILITIES = 0x00A0
E120_LANGUAGE = 0x00B0
E120_SOFTWARE_VERSION_LABEL = 0x00C0
E120_BOOT_SOFTWARE_VERSION_ID = 0x00C1
E120_BOOT_SOFTWARE_VERSION_LABEL = 0x00C2

# Category - DMX512 Setup         */
E120_DMX_PERSONALITY = 0x00E0
E120_DMX_PERSONALITY_DESCRIPTION = 0x00E1
E120_DMX_START_ADDRESS = 0x00F0 # Support required if device uses a DMX512 Slot.             */
E120_SLOT_INFO = 0x0120
E120_SLOT_DESCRIPTION = 0x0121
E120_DEFAULT_SLOT_VALUE = 0x0122
E137_1_DMX_BLOCK_ADDRESS = 0x0140 # Defined in ANSI E1.37-1 document                           */
E137_1_DMX_FAIL_MODE = 0x0141 # Defined in ANSI E1.37-1 document                           */
E137_1_DMX_STARTUP_MODE = 0x0142 # Defined in ANSI E1.37-1 document                           */

# Category - Sensors              */
E120_SENSOR_DEFINITION = 0x0200
E120_SENSOR_VALUE = 0x0201
E120_RECORD_SENSORS = 0x0202

# Category - Dimmer Settings      */
E137_1_DIMMER_INFO = 0x0340
E137_1_MINIMUM_LEVEL = 0x0341
E137_1_MAXIMUM_LEVEL = 0x0342
E137_1_CURVE = 0x0343
E137_1_CURVE_DESCRIPTION = 0x0344 # Support required if CURVE is supported                     */
E137_1_OUTPUT_RESPONSE_TIME = 0x0345
E137_1_OUTPUT_RESPONSE_TIME_DESCRIPTION = 0x0346 # Support required if OUTPUT_RESPONSE_TIME is supported      */
E137_1_MODULATION_FREQUENCY = 0x0347
E137_1_MODULATION_FREQUENCY_DESCRIPTION = 0x0348 # Support required if MODULATION_FREQUENCY is supported      */

# Category - Power/Lamp Settings  */
E120_DEVICE_HOURS = 0x0400
E120_LAMP_HOURS = 0x0401
E120_LAMP_STRIKES = 0x0402
E120_LAMP_STATE = 0x0403 # See Table A-8                                              */
E120_LAMP_ON_MODE = 0x0404 # See Table A-9                                              */
E120_DEVICE_POWER_CYCLES = 0x0405
E137_1_BURN_IN = 0x0440 # Defined in ANSI E1.37-1                                    */

# Category - Display Settings     */
E120_DISPLAY_INVERT = 0x0500
E120_DISPLAY_LEVEL = 0x0501
# Category - Configuration        */
E120_PAN_INVERT = 0x0600
E120_TILT_INVERT = 0x0601
E120_PAN_TILT_SWAP = 0x0602
E120_REAL_TIME_CLOCK = 0x0603
E137_1_LOCK_PIN = 0x0640 # Defined in ANSI E1.37-1                                    */
E137_1_LOCK_STATE = 0x0641 # Defined in ANSI E1.37-1                                    */
E137_1_LOCK_STATE_DESCRIPTION = 0x0642 # Support required if MODULATION_FREQUENCY is supported      */

# Category - Network Configuration*/

E137_2_LIST_INTERFACES = 0x0700 # Defined in ANSI E1.37-2                                    */
E137_2_INTERFACE_LABEL = 0x0701 # Defined in ANSI E1.37-2                                    */
E137_2_INTERFACE_HARDWARE_ADDRESS_TYPE1 = 0x0702 # Defined in ANSI E1.37-2                                    */
E137_2_IPV4_DHCP_MODE = 0x0703 # Defined in ANSI E1.37-2                                    */
E137_2_IPV4_ZEROCONF_MODE = 0x0704 # Defined in ANSI E1.37-2                                    */
E137_2_IPV4_CURRENT_ADDRESS = 0x0705 # Defined in ANSI E1.37-2                                    */
E137_2_IPV4_STATIC_ADDRESS = 0x0706 # Defined in ANSI E1.37-2                                    */
E137_2_INTERFACE_RENEW_DHCP = 0x0707 # Defined in ANSI E1.37-2                                    */
E137_2_INTERFACE_RELEASE_DHCP = 0x0708 # Defined in ANSI E1.37-2                                    */
E137_2_INTERFACE_APPLY_CONFIGURATION = 0x0709 # Defined in ANSI E1.37-2 (Support required if _ADDRESS PIDs supported) */
E137_2_IPV4_DEFAULT_ROUTE = 0x070A # Defined in ANSI E1.37-2                                    */
E137_2_DNS_IPV4_NAME_SERVER = 0x070B # Defined in ANSI E1.37-2                                    */
E137_2_DNS_HOSTNAME = 0x070C # Defined in ANSI E1.37-2                                    */
E137_2_DNS_DOMAIN_NAME = 0x070D # Defined in ANSI E1.37-2                                    */


# Category - Control              */
E120_IDENTIFY_DEVICE = 0x1000
E120_RESET_DEVICE = 0x1001
E120_POWER_STATE = 0x1010 # See Table A-11                                              */
E120_PERFORM_SELFTEST = 0x1020 # See Table A-10                                              */
E120_SELF_TEST_DESCRIPTION = 0x1021
E120_CAPTURE_PRESET = 0x1030
E120_PRESET_PLAYBACK = 0x1031 # See Table A-7                                               */
E137_1_IDENTIFY_MODE = 0x1040 # Defined in ANSI E1.37-1                                     */
E137_1_PRESET_INFO = 0x1041 # Defined in ANSI E1.37-1                                     */
E137_1_PRESET_STATUS = 0x1042 # Defined in ANSI E1.37-1                                     */
E137_1_PRESET_MERGEMODE = 0x1043 # See E1.37-1 Table A-3                                       */
E137_1_POWER_ON_SELF_TEST = 0x1044 # Defined in ANSI E1.37-1                                     */

#****************************************************************/
# Discovery Mute/Un-Mute Messages Control Field. See Table 7-3. */
#****************************************************************/
E120_CONTROL_PROXIED_DEVICE = 0x0008
E120_CONTROL_BOOT_LOADER = 0x0004
E120_CONTROL_SUB_DEVICE = 0x0002
E120_CONTROL_MANAGED_PROXY = 0x0001

#*******************************************************/
# Table A-4: Status Type Defines                       */
#*******************************************************/
E120_STATUS_NONE = 0x00   # Not allowed for use with GET: QUEUED_MESSAGE                */
E120_STATUS_GET_LAST_MESSAGE = 0x01
E120_STATUS_ADVISORY = 0x02
E120_STATUS_WARNING = 0x03
E120_STATUS_ERROR = 0x04
E120_STATUS_ADVISORY_CLEARED = 0x12  # Added in E1.20-2010 version                                  */
E120_STATUS_WARNING_CLEARED = 0x13  # Added in E1.20-2010 version                                  */
E120_STATUS_ERROR_CLEARED = 0x14  # Added in E1.20-2010 version                                  */


#*******************************************************/
# Table A-5: Product Category Defines                  */
#*******************************************************/
E120_PRODUCT_CATEGORY_NOT_DECLARED = 0x0000

# Fixtures - intended as source of illumination See Note 1                                                                     */
E120_PRODUCT_CATEGORY_FIXTURE = 0x0100 # No Fine Category declared                                   */
E120_PRODUCT_CATEGORY_FIXTURE_FIXED = 0x0101 # No pan / tilt / focus style functions                       */
E120_PRODUCT_CATEGORY_FIXTURE_MOVING_YOKE = 0x0102
E120_PRODUCT_CATEGORY_FIXTURE_MOVING_MIRROR = 0x0103
E120_PRODUCT_CATEGORY_FIXTURE_OTHER = 0x01FF # For example, focus but no pan/tilt.                         */

# Fixture Accessories - add-ons to fixtures or projectors                                                                      */
E120_PRODUCT_CATEGORY_FIXTURE_ACCESSORY = 0x0200 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_FIXTURE_ACCESSORY_COLOR = 0x0201 # Scrollers / Color Changers                                  */
E120_PRODUCT_CATEGORY_FIXTURE_ACCESSORY_YOKE = 0x0202 # Yoke add-on                                                 */
E120_PRODUCT_CATEGORY_FIXTURE_ACCESSORY_MIRROR = 0x0203 # Moving mirror add-on                                        */
E120_PRODUCT_CATEGORY_FIXTURE_ACCESSORY_EFFECT = 0x0204 # Effects Discs                                               */
E120_PRODUCT_CATEGORY_FIXTURE_ACCESSORY_BEAM = 0x0205 # Gobo Rotators /Iris / Shutters / Dousers/ Beam modifiers.   */
E120_PRODUCT_CATEGORY_FIXTURE_ACCESSORY_OTHER = 0x02FF

# Projectors - light source capable of producing realistic images from another media i.e Video / Slide / Oil Wheel / Film */
E120_PRODUCT_CATEGORY_PROJECTOR = 0x0300 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_PROJECTOR_FIXED = 0x0301 # No pan / tilt functions.                                    */
E120_PRODUCT_CATEGORY_PROJECTOR_MOVING_YOKE = 0x0302
E120_PRODUCT_CATEGORY_PROJECTOR_MOVING_MIRROR = 0x0303
E120_PRODUCT_CATEGORY_PROJECTOR_OTHER = 0x03FF

# Atmospheric Effect - earth/wind/fire                                                                                         */
E120_PRODUCT_CATEGORY_ATMOSPHERIC = 0x0400 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_ATMOSPHERIC_EFFECT = 0x0401 # Fogger / Hazer / Flame, etc.                                */
E120_PRODUCT_CATEGORY_ATMOSPHERIC_PYRO = 0x0402 # See Note 2.                                                 */
E120_PRODUCT_CATEGORY_ATMOSPHERIC_OTHER = 0x04FF

# Intensity Control (specifically Dimming equipment)                                                                           */
E120_PRODUCT_CATEGORY_DIMMER = 0x0500 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_DIMMER_AC_INCANDESCENT = 0x0501 # AC > 50VAC                                                  */
E120_PRODUCT_CATEGORY_DIMMER_AC_FLUORESCENT = 0x0502
E120_PRODUCT_CATEGORY_DIMMER_AC_COLDCATHODE = 0x0503 # High Voltage outputs such as Neon or other cold cathode.    */
E120_PRODUCT_CATEGORY_DIMMER_AC_NONDIM = 0x0504 # Non-Dim module in dimmer rack.                              */
E120_PRODUCT_CATEGORY_DIMMER_AC_ELV = 0x0505 # AC <= 50V such as 12/24V AC Low voltage lamps.              */
E120_PRODUCT_CATEGORY_DIMMER_AC_OTHER = 0x0506
E120_PRODUCT_CATEGORY_DIMMER_DC_LEVEL = 0x0507 # Variable DC level output.                                   */
E120_PRODUCT_CATEGORY_DIMMER_DC_PWM = 0x0508 # Chopped (PWM) output.                                       */
E120_PRODUCT_CATEGORY_DIMMER_CS_LED = 0x0509 # Specialized LED dimmer.                                     */
E120_PRODUCT_CATEGORY_DIMMER_OTHER = 0x05FF

# Power Control (other than Dimming equipment)                                                                                 */
E120_PRODUCT_CATEGORY_POWER = 0x0600 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_POWER_CONTROL = 0x0601 # Contactor racks, other forms of Power Controllers.          */
E120_PRODUCT_CATEGORY_POWER_SOURCE = 0x0602 # Generators                                                  */
E120_PRODUCT_CATEGORY_POWER_OTHER = 0x06FF

# Scenic Drive - including motorized effects unrelated to light source.                                                        */
E120_PRODUCT_CATEGORY_SCENIC = 0x0700 # No Fine Category declared                                   */
E120_PRODUCT_CATEGORY_SCENIC_DRIVE = 0x0701 # Rotators / Kabuki drops, etc. See Note 2.                   */
E120_PRODUCT_CATEGORY_SCENIC_OTHER = 0x07FF

# DMX Infrastructure, conversion and interfaces                                                                                */
E120_PRODUCT_CATEGORY_DATA = 0x0800 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_DATA_DISTRIBUTION = 0x0801 # Splitters/repeaters/Ethernet products used to distribute DMX*/
E120_PRODUCT_CATEGORY_DATA_CONVERSION = 0x0802 # Protocol Conversion analog decoders.                        */
E120_PRODUCT_CATEGORY_DATA_OTHER = 0x08FF

# Audio-Visual Equipment                                                                                                       */
E120_PRODUCT_CATEGORY_AV = 0x0900 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_AV_AUDIO = 0x0901 # Audio controller or device.                                 */
E120_PRODUCT_CATEGORY_AV_VIDEO = 0x0902 # Video controller or display device.                         */
E120_PRODUCT_CATEGORY_AV_OTHER = 0x09FF

# Parameter Monitoring Equipment See Note 3.                                                                                   */
E120_PRODUCT_CATEGORY_MONITOR = 0x0A00 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_MONITOR_ACLINEPOWER = 0x0A01 # Product that monitors AC line voltage, current or power.    */
E120_PRODUCT_CATEGORY_MONITOR_DCPOWER = 0x0A02 # Product that monitors DC line voltage, current or power.    */
E120_PRODUCT_CATEGORY_MONITOR_ENVIRONMENTAL = 0x0A03 # Temperature or other environmental parameter.               */
E120_PRODUCT_CATEGORY_MONITOR_OTHER = 0x0AFF

# Controllers, Backup devices                                                                                                  */
E120_PRODUCT_CATEGORY_CONTROL = 0x7000 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_CONTROL_CONTROLLER = 0x7001
E120_PRODUCT_CATEGORY_CONTROL_BACKUPDEVICE = 0x7002
E120_PRODUCT_CATEGORY_CONTROL_OTHER = 0x70FF

# Test Equipment                                                                                                               */
E120_PRODUCT_CATEGORY_TEST = 0x7100 # No Fine Category declared.                                  */
E120_PRODUCT_CATEGORY_TEST_EQUIPMENT = 0x7101

E120_PRODUCT_CATEGORY_TEST_EQUIPMENT_OTHER = 0x71FF

# Miscellaneous                                                                                                                */
E120_PRODUCT_CATEGORY_OTHER = 0x7FFF # For devices that aren't described within this table.        */


#*******************************************************/
# Table A-6: Product Detail Defines                    */
#*******************************************************/

E120_PRODUCT_DETAIL_NOT_DECLARED = 0x0000

# Generally applied to fixtures                                                                                                */
E120_PRODUCT_DETAIL_ARC = 0x0001
E120_PRODUCT_DETAIL_METAL_HALIDE = 0x0002
E120_PRODUCT_DETAIL_INCANDESCENT = 0x0003
E120_PRODUCT_DETAIL_LED = 0x0004
E120_PRODUCT_DETAIL_FLUROESCENT = 0x0005
E120_PRODUCT_DETAIL_COLDCATHODE = 0x0006  #includes Neon/Argon                                         */
E120_PRODUCT_DETAIL_ELECTROLUMINESCENT = 0x0007
E120_PRODUCT_DETAIL_LASER = 0x0008
E120_PRODUCT_DETAIL_FLASHTUBE = 0x0009 # Strobes or other flashtubes                                 */

# Generally applied to fixture accessories                                                                                     */
E120_PRODUCT_DETAIL_COLORSCROLLER = 0x0100
E120_PRODUCT_DETAIL_COLORWHEEL = 0x0101
E120_PRODUCT_DETAIL_COLORCHANGE = 0x0102 # Semaphore or other type                                     */
E120_PRODUCT_DETAIL_IRIS_DOUSER = 0x0103
E120_PRODUCT_DETAIL_DIMMING_SHUTTER = 0x0104
E120_PRODUCT_DETAIL_PROFILE_SHUTTER = 0x0105 # hard-edge beam masking                                      */
E120_PRODUCT_DETAIL_BARNDOOR_SHUTTER = 0x0106 # soft-edge beam masking                                      */
E120_PRODUCT_DETAIL_EFFECTS_DISC = 0x0107
E120_PRODUCT_DETAIL_GOBO_ROTATOR = 0x0108

# Generally applied to Projectors                                                                                              */
E120_PRODUCT_DETAIL_VIDEO = 0x0200
E120_PRODUCT_DETAIL_SLIDE = 0x0201
E120_PRODUCT_DETAIL_FILM = 0x0202
E120_PRODUCT_DETAIL_OILWHEEL = 0x0203
E120_PRODUCT_DETAIL_LCDGATE = 0x0204

# Generally applied to Atmospheric Effects                                                                                     */
E120_PRODUCT_DETAIL_FOGGER_GLYCOL = 0x0300 # Glycol/Glycerin hazer                                       */
E120_PRODUCT_DETAIL_FOGGER_MINERALOIL = 0x0301 # White Mineral oil hazer                                     */
E120_PRODUCT_DETAIL_FOGGER_WATER = 0x0302 # Water hazer                                                 */
E120_PRODUCT_DETAIL_C02 = 0x0303 # Dry Ice/Carbon Dioxide based                                */
E120_PRODUCT_DETAIL_LN2 = 0x0304 # Nitrogen based                                              */
E120_PRODUCT_DETAIL_BUBBLE = 0x0305 # including foam                                              */
E120_PRODUCT_DETAIL_FLAME_PROPANE = 0x0306
E120_PRODUCT_DETAIL_FLAME_OTHER = 0x0307
E120_PRODUCT_DETAIL_OLEFACTORY_STIMULATOR = 0x0308 # Scents                                                      */
E120_PRODUCT_DETAIL_SNOW = 0x0309
E120_PRODUCT_DETAIL_WATER_JET = 0x030A # Fountain controls etc                                       */
E120_PRODUCT_DETAIL_WIND = 0x030B # Air Mover                                                   */
E120_PRODUCT_DETAIL_CONFETTI = 0x030C
E120_PRODUCT_DETAIL_HAZARD = 0x030D # Any form of pyrotechnic control or device.                  */

# Generally applied to Dimmers/Power controllers See Note 1                                                                    */
E120_PRODUCT_DETAIL_PHASE_CONTROL = 0x0400
E120_PRODUCT_DETAIL_REVERSE_PHASE_CONTROL = 0x0401 # includes FET/IGBT                                           */
E120_PRODUCT_DETAIL_SINE = 0x0402
E120_PRODUCT_DETAIL_PWM = 0x0403
E120_PRODUCT_DETAIL_DC = 0x0404 # Variable voltage                                            */
E120_PRODUCT_DETAIL_HFBALLAST = 0x0405 # for Fluroescent                                             */
E120_PRODUCT_DETAIL_HFHV_NEONBALLAST = 0x0406 # for Neon/Argon and other coldcathode.                       */
E120_PRODUCT_DETAIL_HFHV_EL = 0x0407 # for Electroluminscent                                       */
E120_PRODUCT_DETAIL_MHR_BALLAST = 0x0408 # for Metal Halide                                            */
E120_PRODUCT_DETAIL_BITANGLE_MODULATION = 0x0409
E120_PRODUCT_DETAIL_FREQUENCY_MODULATION = 0x040A
E120_PRODUCT_DETAIL_HIGHFREQUENCY_12V = 0x040B # as commonly used with MR16 lamps                            */
E120_PRODUCT_DETAIL_RELAY_MECHANICAL = 0x040C # See Note 1                                                  */
E120_PRODUCT_DETAIL_RELAY_ELECTRONIC = 0x040D # See Note 1, Note 2                                          */
E120_PRODUCT_DETAIL_SWITCH_ELECTRONIC = 0x040E # See Note 1, Note 2                                          */
E120_PRODUCT_DETAIL_CONTACTOR = 0x040F # See Note 1                                                  */

# Generally applied to Scenic drive                                                                                            */
E120_PRODUCT_DETAIL_MIRRORBALL_ROTATOR = 0x0500
E120_PRODUCT_DETAIL_OTHER_ROTATOR = 0x0501 # includes turntables                                         */
E120_PRODUCT_DETAIL_KABUKI_DROP = 0x0502
E120_PRODUCT_DETAIL_CURTAIN = 0x0503 # flown or traveller                                          */
E120_PRODUCT_DETAIL_LINESET = 0x0504
E120_PRODUCT_DETAIL_MOTOR_CONTROL = 0x0505
E120_PRODUCT_DETAIL_DAMPER_CONTROL = 0x0506 # HVAC Damper                                                 */

# Generally applied to Data Distribution                                                                                       */
E120_PRODUCT_DETAIL_SPLITTER = 0x0600 # Includes buffers/repeaters                                  */
E120_PRODUCT_DETAIL_ETHERNET_NODE = 0x0601 # DMX512 to/from Ethernet                                     */
E120_PRODUCT_DETAIL_MERGE = 0x0602 # DMX512 combiner                                             */
E120_PRODUCT_DETAIL_DATAPATCH = 0x0603 # Electronic Datalink Patch                                   */
E120_PRODUCT_DETAIL_WIRELESS_LINK = 0x0604 # radio/infrared                                              */

# Generally applied to Data Conversion and Interfaces                                                                          */
E120_PRODUCT_DETAIL_PROTOCOL_CONVERTOR = 0x0701 # D54/AMX192/Non DMX serial links, etc to/from DMX512         */
E120_PRODUCT_DETAIL_ANALOG_DEMULTIPLEX = 0x0702 # DMX to DC voltage                                           */
E120_PRODUCT_DETAIL_ANALOG_MULTIPLEX = 0x0703 # DC Voltage to DMX                                           */
E120_PRODUCT_DETAIL_SWITCH_PANEL = 0x0704 # Pushbuttons to DMX or polled using RDM                      */

# Generally applied to Audio or Video (AV) devices                                                                             */
E120_PRODUCT_DETAIL_ROUTER = 0x0800 # Switching device                                            */
E120_PRODUCT_DETAIL_FADER = 0x0801 # Single channel                                              */
E120_PRODUCT_DETAIL_MIXER = 0x0802 # Multi-channel                                               */

# Generally applied to Controllers, Backup devices and Test Equipment                                                          */
E120_PRODUCT_DETAIL_CHANGEOVER_MANUAL = 0x0900 # requires manual intervention to assume control of DMX line   */
E120_PRODUCT_DETAIL_CHANGEOVER_AUTO = 0x0901 # may automatically assume control of DMX line                 */
E120_PRODUCT_DETAIL_TEST = 0x0902 # test equipment                                               */

# Could be applied to any category                                                                                             */
E120_PRODUCT_DETAIL_GFI_RCD = 0x0A00 # device includes GFI/RCD trip                                 */
E120_PRODUCT_DETAIL_BATTERY = 0x0A01 # device is battery operated                                   */
E120_PRODUCT_DETAIL_CONTROLLABLE_BREAKER = 0x0A02


E120_PRODUCT_DETAIL_OTHER = 0x7FFF # for use where the Manufacturer believes that none of the


# Note 1: Products intended for switching 50V AC / 120V DC or greater should be declared with a
#           Product Category of PRODUCT_CATEGORY_POWER_CONTROL.

#           Products only suitable for extra low voltage switching (typically up to 50VAC / 30VDC) at currents
#           less than 1 ampere should be declared with a Product Category of PRODUCT_CATEGORY_DATA_CONVERSION.#
#
#           Please refer to GET: DEVICE_INFO and Table A-5 for an explanation of Product Category declaration.
#   Note 2: Products with TTL, MOSFET or Open Collector Transistor Outputs or similar non-isolated electronic
#           outputs should be declared as PRODUCT_DETAIL_SWITCH_ELECTRONIC. Use of PRODUCT_DETAIL_RELAY_ELECTRONIC
#           shall be restricted to devices whereby the switched circuits are electrically isolated from the control signals.     */


#*******************************************************/
# Table A-7: Preset Playback Defines                   */
#*******************************************************/

E120_PRESET_PLAYBACK_OFF = 0x0000 # Returns to Normal DMX512 Input                               */
E120_PRESET_PLAYBACK_ALL = 0xFFFF # Plays Scenes in Sequence if supported.                       */
#      E120_PRESET_PLAYBACK_SCENE                       0x0001-


#*******************************************************/
# Table A-8: Lamp State Defines                        */
#*******************************************************/

E120_LAMP_OFF = 0x00   # No demonstrable light output                                 */
E120_LAMP_ON = 0x01
E120_LAMP_STRIKE = 0x02   # Arc-Lamp ignite                                              */
E120_LAMP_STANDBY = 0x03   # Arc-Lamp Reduced Power Mode                                  */
E120_LAMP_NOT_PRESENT = 0x04   # Lamp not installed                                           */
E120_LAMP_ERROR = 0x7F
# Manufacturer-Specific States                          0x80-                                    */

#*******************************************************/
# Table A-9: Lamp On Mode Defines                      */
#*******************************************************/

E120_LAMP_ON_MODE_OFF = 0x00   # Lamp Stays off until directly instructed to Strike.          */
E120_LAMP_ON_MODE_DMX = 0x01   # Lamp Strikes upon receiving a DMX512 signal.                 */
E120_LAMP_ON_MODE_ON = 0x02   # Lamp Strikes automatically at Power-up.                      */
E120_LAMP_ON_MODE_AFTER_CAL = 0x03   # Lamp Strikes after Calibration or Homing procedure.          */
# Manufacturer-Specific Modes                           0x80-
                                                              

#*******************************************************/
# Table A-10: Self Test Defines                        */
#*******************************************************/

E120_SELF_TEST_OFF = 0x00   # Turns Self Tests Off                                         */

E120_SELF_TEST_ALL = 0xFF   # Self Test All, if applicable                                 */

#*******************************************************/
# Table A-11: Power State Defines                      */
#*******************************************************/

E120_POWER_STATE_FULL_OFF = 0x00   # Completely disengages power to device. Device can no longer respond. */
E120_POWER_STATE_SHUTDOWN = 0x01   # Reduced power mode, may require device reset to return to
E120_POWER_STATE_STANDBY = 0x02   # Reduced power mode. Device can return to NORMAL without a
E120_POWER_STATE_NORMAL = 0xFF   # Normal Operating Mode.                                       */

#*******************************************************/
# Table A-12: Sensor Type Defines                      */
#*******************************************************/

E120_SENS_TEMPERATURE = 0x00
E120_SENS_VOLTAGE = 0x01
E120_SENS_CURRENT = 0x02
E120_SENS_FREQUENCY = 0x03
E120_SENS_RESISTANCE = 0x04   # Eg: Cable resistance                                         */
E120_SENS_POWER = 0x05
E120_SENS_MASS = 0x06   # Eg: Truss load Cell                                          */
E120_SENS_LENGTH = 0x07
E120_SENS_AREA = 0x08
E120_SENS_VOLUME = 0x09   # Eg: Smoke Fluid                                              */
E120_SENS_DENSITY = 0x0A
E120_SENS_VELOCITY = 0x0B
E120_SENS_ACCELERATION = 0x0C
E120_SENS_FORCE = 0x0D
E120_SENS_ENERGY = 0x0E
E120_SENS_PRESSURE = 0x0F
E120_SENS_TIME = 0x10
E120_SENS_ANGLE = 0x11
E120_SENS_POSITION_X = 0x12   # E.g.: Lamp position on Truss                                 */
E120_SENS_POSITION_Y = 0x13
E120_SENS_POSITION_Z = 0x14
E120_SENS_ANGULAR_VELOCITY = 0x15   # E.g.: Wind speed                                             */
E120_SENS_LUMINOUS_INTENSITY = 0x16
E120_SENS_LUMINOUS_FLUX = 0x17
E120_SENS_ILLUMINANCE = 0x18
E120_SENS_CHROMINANCE_RED = 0x19
E120_SENS_CHROMINANCE_GREEN = 0x1A
E120_SENS_CHROMINANCE_BLUE = 0x1B
E120_SENS_CONTACTS = 0x1C   # E.g.: Switch inputs.                                         */
E120_SENS_MEMORY = 0x1D   # E.g.: ROM Size                                               */
E120_SENS_ITEMS = 0x1E   # E.g.: Scroller gel frames.                                   */
E120_SENS_HUMIDITY = 0x1F
E120_SENS_COUNTER_16BIT = 0x20
E120_SENS_OTHER = 0x7F
# Manufacturer-Specific Sensors                         0x80-

#*******************************************************/
# Table A-13: Sensor Unit Defines                      */
#*******************************************************/

E120_UNITS_NONE = 0x00   # CONTACTS                                                     */
E120_UNITS_CENTIGRADE = 0x01   # TEMPERATURE	                                                */
E120_UNITS_VOLTS_DC = 0x02   # VOLTAGE                                                      */
E120_UNITS_VOLTS_AC_PEAK = 0x03   # VOLTAGE                                                      */
E120_UNITS_VOLTS_AC_RMS = 0x04   # VOLTAGE                                                      */
E120_UNITS_AMPERE_DC = 0x05   # CURRENT                                                      */
E120_UNITS_AMPERE_AC_PEAK = 0x06   # CURRENT                                                      */
E120_UNITS_AMPERE_AC_RMS = 0x07   # CURRENT                                                      */
E120_UNITS_HERTZ = 0x08   # FREQUENCY / ANG_VEL                                          */
E120_UNITS_OHM = 0x09   # RESISTANCE                                                   */
E120_UNITS_WATT = 0x0A   # POWER                                                        */
E120_UNITS_KILOGRAM = 0x0B   # MASS                                                         */
E120_UNITS_METERS = 0x0C   # LENGTH / POSITION                                            */
E120_UNITS_METERS_SQUARED = 0x0D   # AREA                                                         */
E120_UNITS_METERS_CUBED = 0x0E   # VOLUME                                                       */
E120_UNITS_KILOGRAMMES_PER_METER_CUBED = 0x0F   # DENSITY                                                      */
E120_UNITS_METERS_PER_SECOND = 0x10   # VELOCITY                                                     */
E120_UNITS_METERS_PER_SECOND_SQUARED = 0x11   # ACCELERATION	                                                */
E120_UNITS_NEWTON = 0x12   # FORCE                                                        */
E120_UNITS_JOULE = 0x13   # ENERGY                                                       */
E120_UNITS_PASCAL = 0x14   # PRESSURE                                                     */
E120_UNITS_SECOND = 0x15   # TIME                                                         */
E120_UNITS_DEGREE = 0x16   # ANGLE                                                        */
E120_UNITS_STERADIAN = 0x17   # ANGLE                                                        */
E120_UNITS_CANDELA = 0x18   # LUMINOUS_INTENSITY                                           */
E120_UNITS_LUMEN = 0x19   # LUMINOUS_FLUX                                                */
E120_UNITS_LUX = 0x1A   # ILLUMINANCE                                                  */
E120_UNITS_IRE = 0x1B   # CHROMINANCE                                                  */
E120_UNITS_BYTE = 0x1C   # MEMORY                                                       */
# Manufacturer-Specific Units                           0x80-


#*******************************************************/
# Table A-14: Sensor Unit Prefix Defines               */
#*******************************************************/

E120_PREFIX_NONE = 0x00   # Multiply by 1                                                */
E120_PREFIX_DECI = 0x01   # Multiply by 10-1                                             */
E120_PREFIX_CENTI = 0x02   # Multiply by 10-2                                             */
E120_PREFIX_MILLI = 0x03   # Multiply by 10-3                                             */
E120_PREFIX_MICRO = 0x04   # Multiply by 10-6                                             */
E120_PREFIX_NANO = 0x05   # Multiply by 10-9                                             */
E120_PREFIX_PICO = 0x06   # Multiply by 10-12                                            */
E120_PREFIX_FEMPTO = 0x07   # Multiply by 10-15                                            */
E120_PREFIX_ATTO = 0x08   # Multiply by 10-18                                            */
E120_PREFIX_ZEPTO = 0x09   # Multiply by 10-21                                            */
E120_PREFIX_YOCTO = 0x0A   # Multiply by 10-24                                            */
E120_PREFIX_DECA = 0x11   # Multiply by 10+1                                             */
E120_PREFIX_HECTO = 0x12   # Multiply by 10+2                                             */
E120_PREFIX_KILO = 0x13   # Multiply by 10+3                                             */
E120_PREFIX_MEGA = 0x14   # Multiply by 10+6                                             */
E120_PREFIX_GIGA = 0x15   # Multiply by 10+9                                             */
E120_PREFIX_TERRA = 0x16   # Multiply by 10+12                                            */
E120_PREFIX_PETA = 0x17   # Multiply by 10+15                                            */
E120_PREFIX_EXA = 0x18   # Multiply by 10+18                                            */
E120_PREFIX_ZETTA = 0x19   # Multiply by 10+21                                            */
E120_PREFIX_YOTTA = 0x1A   # Multiply by 10+24                                            */


#*******************************************************/
# Table A-15: Data Type Defines                        */
#*******************************************************/

E120_DS_NOT_DEFINED = 0x00   # Data type is not defined                                     */
E120_DS_BIT_FIELD = 0x01   # Data is bit packed                                           */
E120_DS_ASCII = 0x02   # Data is a string                                             */
E120_DS_UNSIGNED_BYTE = 0x03   # Data is an array of unsigned bytes                           */
E120_DS_SIGNED_BYTE = 0x04   # Data is an array of signed bytes                             */
E120_DS_UNSIGNED_WORD = 0x05   # Data is an array of unsigned 16-bit words                    */
E120_DS_SIGNED_WORD = 0x06   # Data is an array of signed 16-bit words                      */
E120_DS_UNSIGNED_DWORD = 0x07   # Data is an array of unsigned 32-bit words                    */
E120_DS_SIGNED_DWORD = 0x08   # Data is an array of signed 32-bit words                      */
# Manufacturer-Specific Data Types                      0x80-                                                                  */
#                                                       0xDF                                                                   */

#*******************************************************/
# Table A-16: Parameter Desc. Command Class Defines    */
#*******************************************************/

E120_CC_GET = 0x01   # PID supports GET only                                        */
E120_CC_SET = 0x02   # PID supports SET only                                        */
E120_CC_GET_SET = 0x03   # PID supports GET & SET                                       */

#*******************************************************/
# Table A-17: Response NACK Reason Code Defines        */
#*******************************************************/

E120_NR_UNKNOWN_PID = 0x0000 # The responder cannot comply with request because the message is not implemented in responder.                             */
E120_NR_FORMAT_ERROR = 0x0001 # The responder cannot interpret request as controller data was not formatted correctly.                                 */
E120_NR_HARDWARE_FAULT = 0x0002 # The responder cannot comply due to an internal hardware fault*/
E120_NR_PROXY_REJECT = 0x0003 # Proxy is not the RDM line master and cannot comply with message.*/
E120_NR_WRITE_PROTECT = 0x0004 # SET Command normally allowed but being blocked currently.    */
E120_NR_UNSUPPORTED_COMMAND_CLASS = 0x0005 # Not valid for Command Class attempted. May be used where GET allowed but SET is not supported.                        */
E120_NR_DATA_OUT_OF_RANGE = 0x0006 # Value for given Parameter out of allowable range or not supported.                                               */
E120_NR_BUFFER_FULL = 0x0007 # Buffer or Queue space currently has no free space to store data. */
E120_NR_PACKET_SIZE_UNSUPPORTED = 0x0008 # Incoming message exceeds buffer capacity.                    */
E120_NR_SUB_DEVICE_OUT_OF_RANGE = 0x0009 # Sub-Device is out of range or unknown.                       */
E120_NR_PROXY_BUFFER_FULL = 0x000A # Proxy buffer is full and can not store any more Queued       */
                                                            # Message or Status Message responses.                         */
E137_2_NR_ACTION_NOT_SUPPORTED = 0x000B # The parameter data is valid but the SET operation cannot be  */
                                                            # performed with the current configuration.                    */

#*******************************************************************************************************************************/
#*******************************************************************************************************************************/
# ANSI E1.37-1 DEFINES                                                                                                         */
#*******************************************************************************************************************************/
#*******************************************************************************************************************************/

#*******************************************************/
# E1.37-1 Table A-2: Preset Programmed Defines         */
#*******************************************************/
E137_1_PRESET_NOT_PROGRAMMED = 0x00 # Preset Scene not programmed.                                   */
E137_1_PRESET_PROGRAMMED = 0x01 # Preset Scene programmed.                                       */
E137_1_PRESET_PROGRAMMED_READ_ONLY = 0x02 # Preset Scene read-only, factory programmed.                    */

#*******************************************************/
# E1.37-1 Table A-3: Merge Mode Defines                */
#*******************************************************/
E137_1_MERGEMODE_DEFAULT = 0x00 # Preset overrides DMX512 default behavior as defined in         */
                                                            # E1.20 PRESET_PLAYBACK                                          */
E137_1_MERGEMODE_HTP = 0x01 # Highest Takes Precedence on slot by slot basis                 */
E137_1_MERGEMODE_LTP = 0x02 # Latest Takes Precedence from Preset or DMX512 on slot by slot  */
E137_1_MERGEMODE_DMX_ONLY = 0x03 # DMX512 only, Preset ignored                                    */
E137_1_MERGEMODE_OTHER = 0xFF # Other (undefined) merge mode                                   */


#*******************************************************************************************************************************/
#*******************************************************************************************************************************/
# ANSI E1.37-2 DEFINES                                                                                                         */
#*******************************************************************************************************************************/
#*******************************************************************************************************************************/

#*******************************************************/
# E1.37-2 Table A-3: DHCP Mode Defines                 */
#*******************************************************/
E137_2_DHCP_MODE_INACTIVE = 0x00 # IP Address was not obtained via DHCP                           */
E137_2_DHCP_MODE_ACTIVE = 0x01 # IP Address was obtained via DHCP                               */
E137_2_DHCP_MODE_UNKNOWN = 0x02 # The system cannot determine if address was obtained via DHCP.  */






#*******************************************************/
# Appendix C: Slot Info (Normative)        */
#*******************************************************/

#*******************************************************/
# Table C-1: Slot Type        */
#*******************************************************/

E120_SD_INTENSITY = 0x00 # Slot directly controls parameter (represents Coarsefor 16-bit 
                                                
E120_ST_SEC_FINE = 0x01 # Fine, for 16-bit parameters                                    */
E120_ST_SEC_TIMING = 0x02 # Slot sets timing value for associated parameter                */
E120_ST_SEC_SPEED = 0x03 # Slot sets speed/velocity for associated parameter              */
E120_ST_SEC_CONTROL = 0x04 # Slot provides control/mode info for parameter                  */
E120_ST_SEC_INDEX = 0x05 # Slot sets index position for associated parameter              */
E120_ST_SEC_ROTATION = 0x06 # Slot sets rotation speed for associated parameter              */
E120_ST_SEC_INDEX_ROTATE = 0x07 # Combined index/rotation control                                */

E120_ST_SEC_UNDEFINED = 0xFF # Undefined secondary type                                       */


#*******************************************************/
# Table C-2: Slot ID Definitions        */
#*******************************************************/
#Intensity Functions                                  0x00xx
E120_ST_PRIMARY = 0x0001 # Intensity                                                      */
E120_SD_INTENSITY_MASTER = 0x0002 # Intensity Master                                               */
#Color Functions                                      0x02xx
E120_SD_COLOR_CORRECTION = 0x0208 # Color Temperature Correction