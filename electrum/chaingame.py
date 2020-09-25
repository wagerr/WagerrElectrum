import sys
import struct

BTX_HEX_PREFIX = "42"
QUICK_GAME_BTX_TYPE = "\x0d"
BTX_FORMAT_VERSION = "\x01"

DICE_OP_MIN_STRLEN = 12
DICE_OP_MAX_STRLEN = 20
DICE_GAME_OPCODES = {"EQUAL": "00", "NOTEQUAL": "01", "TOTALOVER":"02", "TOTALUNDER":"03", "EVEN":"04", "ODD":"05" }

class ChainGame:
    def __init__(self):
        super().__init__()
        

    @staticmethod
    def DiceToOpCode(d):
        
        if d.side in ["EQUAL","NOTEQUAL","TOTALUNDER","TOTALOVER"]:
            byte_length = "05"
            Outcome = struct.pack('<i', d.outcome).hex()
        elif d.side in ["EVEN","ODD"]:
            byte_length = "01"
            Outcome=""
        else:
            raise Exception('Invalid Vector Type')
        
        diceGameType = DICE_GAME_OPCODES[d.side]
        opCode = BTX_HEX_PREFIX + "010d00" + byte_length + diceGameType + Outcome 

        if len(opCode) != DICE_OP_MIN_STRLEN and len(opCode) != DICE_OP_MAX_STRLEN :
            return False, opCode
        return True, opCode
    
    @staticmethod
    def DiceFromOpCode(opCode):
        dice = {}
        if(len(opCode) != (DICE_OP_MAX_STRLEN / 2) and len(opCode) != (DICE_OP_MIN_STRLEN / 2) ):
            print("Error: Dice Tx OpCode Length Mismatch")
            return False, dice

        if(opCode[2] != QUICK_GAME_BTX_TYPE):
            print("Error: Quickgame BTX Type Mismatch")
            return False,dice
        
        if(opCode[3] != "00"):
            print("Error: Dice Tx Type Mismatch")
            return False,dice
        
        if (ChainGame.ReadBTXFormatVersion(opCode) != BTX_FORMAT_VERSION):
            print("Error: Dice Tx Version Mismatch")    
            return False,dice

        game_opcode_int = int.from_bytes((opCode[5]).encode('cp437'), "big")
        dice.side = list(DICE_GAME_OPCODES.keys())[list(DICE_GAME_OPCODES.values()).index(game_opcode_int)]
        
        if dice.side in ["EQUAL","NOTEQUAL","TOTALUNDER","TOTALOVER"]:
            dice.outcome = int.from_bytes((opCode[6]+opCode[7]+opCode[8]+opCode[9]).encode('cp437'), byteorder='little', signed=False)
        else:
            dice.outcome = None 
        return True, dice

    def ReadBTXFormatVersion(self, opCode):
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