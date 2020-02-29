import sys
import struct

BTX_HEX_PREFIX = "42"
PB_OP_STRLEN = 16  
plBetTxType = "\x03"
BTX_FORMAT_VERSION = "\x01" 

class PeerlessBet:
    def __init__(self, eventId, outcomeType):
        if eventId is None:
            raise Exception('Empty Event Id')
        self.eventId = eventId
        if outcomeType is None:
            raise Exception('Empty Outcome Type')
        self.outcomeType = outcomeType

    @staticmethod
    def ToOpCode(pb):
        eventId = struct.pack('<i', pb.eventId).hex()
        outcomeType = hex(pb.outcomeType).lstrip("0x").zfill(2)
        opCode = BTX_HEX_PREFIX + "0103" + eventId + outcomeType
        #Ensure peerless bet OpCode string is the correct length.
        if len(opCode) != PB_OP_STRLEN :
            return False,opCode
        return True,opCode

    @staticmethod
    def FromOpCode(opCode) :
        #Ensure peerless bet OpCode string is the correct length.
        pb = PeerlessBet(0,0)
        if (len(opCode) != PB_OP_STRLEN / 2):
            print("Error: Betting Tx OpCode Length Mismatch")
            return False,pb
    
        if (opCode[2] != plBetTxType):
            print("Error: Betting Tx Type Mismatch")
            return False,pb
    
        #Ensure the peerless bet OpCode has the correct BTX format version number.
        if (PeerlessBet.ReadBTXFormatVersion(opCode) != BTX_FORMAT_VERSION):
            print("Error: Betting Tx Version Mismatch")    
            return False,pb

        pb.eventId=int.from_bytes((opCode[3]+opCode[4]+opCode[5]+opCode[6]).encode('cp437'), byteorder='little', signed=False)
        pb.outcomeType = int.from_bytes(opCode[7].encode('cp437'), "big")

        return True,pb
   
    def ReadBTXFormatVersion(opCode):
        #Check the first three bytes match the "BTX" format specification.
        if (opCode[0] != 'B'):
            return -1
        
        bb = opCode[1]
        v = int.from_bytes(opCode[1].encode('utf-8'), "big") 
        # Versions outside the range [1, 254] are not supported.
        if v < 1 or v > 254:
            return -1
        else:
            return opCode[1]