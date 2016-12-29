import pi_switch


def createRF():
    rf = pi_switch.RCSwitchSender()
    rf.enableTransmit(0)
    rf.setPulseLength(194)
    return rf

if __name__ == "__main__":
    rf = createRF()
    print("sending code 1398067")
    rf.sendDecimal(1398067, 24)

