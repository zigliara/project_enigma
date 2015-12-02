# Project Enigma - Python 2.7.10# Emulate the Enigma Machine# coding: asciiimport sys"""Based on info from:1. http://www.matematiksider.dk/enigma_eng.html2. https://en.wikipedia.org/wiki/Enigma_rotor_detailsConstraints:Emulates the Enigma M4 (1942) (Rotors I, II and III and Reflector B-wide)according to link 2Handles 26 capital letters.Wheel l: Left, rotor1Wheel M: Midlle, rotor2Wheel R: Right, rotor3Wheel L will rotate 1/26 each time a new character is entered.Stepping & double-stepping implementedNo plugboard implemented.Spaces will be removed from the input strings.""""""Configuration:Wheel L (Rotor I) configuration:EKMFLGDQVZNTOWYHXUSPAIBRCJTurn-over notch position: 'Q'Wheel M (Rotor II) configuration:AJDKSIRUXBLHWTMCQGZNPYFVOETurn-over notch position: 'E'Wheel R (Rotor III) configuration:BDFHJLCPRTXVZNYEIWGAKMUSQOTurn-over notch position: 'V'Reflector B-wide configuration:YRUHQSLDPXNGOKMIEBFZCWVJAT"""class Rotor(object):    my_rotor = []    def __init__(self, my_wheel, my_setting):        self.my_wheel = my_wheel         alphabet = [chr(i) for i in range(65, 91)]                # Rotor configuration        rotor_1 = 'EKMFLGDQVZNTOWYHXUSPAIBRCJ'        rotor_1_notch = 'Q'        rotor_2 = 'AJDKSIRUXBLHWTMCQGZNPYFVOE'        rotor_2_notch = 'E'        rotor_3 = 'BDFHJLCPRTXVZNYEIWGAKMUSQO'        rotor_3_notch = 'V'        rotor_4 = 'ESOVPZJAYQUIRHXLNFTGKDCMWB'        rotor_4_notch = 'J'        rotor_5 = 'VZBRGITYUPSDNHLXAWMJQOFECK'        rotor_5_notch = 'Z'                # Reflector configuration        reflector_b = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'        reflector_c = 'FVPJIAOYEDRZXWGCTKUQSBNMHL'                if my_wheel == 1:             list_rotor = rotor_1            self.my_notch = rotor_1_notch        elif my_wheel == 2:             list_rotor = rotor_2            self.my_notch = rotor_2_notch        elif my_wheel == 3:             list_rotor = rotor_3            self.my_notch = rotor_3_notch        elif my_wheel == 4:             list_rotor = rotor_4            self.my_notch = rotor_4_notch        elif my_wheel == 5:             list_rotor = rotor_5            self.my_notch = rotor_5_notch        elif my_wheel == 10:             list_rotor = reflector_b            self.my_notch = ''        elif my_wheel == 11:             list_rotor = reflector_c            self.my_notch = ''                # Set the ring setting        diff_list = range(26)        temp_list = range(26)        rotor_config = []                # Get the index differences between the alphabet and the inner-ring        for i in range(26):            rotor_config.append(list_rotor[i])            diff_list[i] = ord(rotor_config[i]) - ord(alphabet[i])        # Build the new setting        for i in range(26):            # Shift the list by as much as the ring setting            if i - my_setting >= 0:                temp_list[i] = diff_list[i - my_setting]            else:                temp_list[i] = diff_list[i - my_setting + len(diff_list)]                        # Assign the correct letters with regards to the shift index            if ord(alphabet[i]) + temp_list[i] < 65:                temp_list[i] = chr(ord(alphabet[i]) + temp_list[i] + 26)            elif ord(alphabet[i]) + temp_list[i] > 90:                temp_list[i] = chr(ord(alphabet[i]) + temp_list[i] - 26)            else:                temp_list[i] = chr(ord(alphabet[i]) + temp_list[i])        rotor_config = temp_list        self.my_rotor = zip(alphabet, rotor_config)# Get the rotor setupdef get_rotor_setup():    pos_rotor_one = 0    pos_rotor_two = 0    pos_rotor_three = 0    pos_reflector = 0    rotor_list = ['I', 'II', 'III', 'IV', 'V', '', '', '', '', 'B', 'C']    chosen_config = []    while pos_rotor_one == 0:        pos_rotor = raw_input('Which rotor do you want to use for the Right position? (I -> V) ')        if pos_rotor in rotor_list:            pos_rotor_one = rotor_list.index(pos_rotor) + 1        else:            print 'Please answer with I, II, II, IV or V.'            while pos_rotor_two == 0:        pos_rotor = raw_input('Which rotor do you want to use for the Middle position? (I -> V) ')        if pos_rotor in rotor_list:            pos_rotor_two = rotor_list.index(pos_rotor) + 1            if pos_rotor_two == pos_rotor_one:                print 'You are not allowed to choose the same rotor for multiple positions.'                pos_rotor_two = 0        else:            print 'Please answer with I, II, III, IV or V.'    while pos_rotor_three == 0:        pos_rotor = raw_input('Which rotor do you want to use for the Left position? (I -> V) ')        if pos_rotor in rotor_list:            pos_rotor_three = rotor_list.index(pos_rotor) + 1            if pos_rotor_three == pos_rotor_two or pos_rotor_three == pos_rotor_one:                print 'You are not allowed to choose the same rotor for multiple positions.'                pos_rotor_three = 0        else:            print 'Please answer with I, II, II, IV or V.'                while pos_reflector == 0:        pos_rotor = raw_input('Which reflector do you want to use (B or C)? ')        if pos_rotor in rotor_list:            pos_reflector = rotor_list.index(pos_rotor) + 1        else:            print 'Please answer with B or C.'                return pos_rotor_one, pos_rotor_two, pos_rotor_three, pos_reflector    # Get rotor offset configuration from the userdef get_start_index():    pos_one = 0    pos_two = 0    pos_three = 0    alphabet = [chr(i) for i in range(65, 91)]    while True:        wheel_r = raw_input('Which position shall the R-rotor start from? ')        if wheel_r.upper() in alphabet:            pos_one = alphabet.index(wheel_r.upper())        wheel_m = raw_input('Which position shall the M-rotor start from? ')        if wheel_m.upper() in alphabet:            pos_two = alphabet.index(wheel_m.upper())        wheel_l = raw_input('Which position shall the L-rotor start from? ')        if wheel_l.upper() in alphabet:            pos_three = alphabet.index(wheel_l.upper())        return pos_one, pos_two, pos_three# Get ring setting configuration from the user for the chosen ringsdef get_ring_setting_index():    ring_setting_one = 0    ring_setting_two = 0    ring_setting_three = 0    alphabet = [chr(i) for i in range(65, 91)]    while True:        wheel_r = raw_input('Which ring-setting shall the R-rotor be set to? ')        if wheel_r.upper() in alphabet:            ring_setting_one = alphabet.index(wheel_r.upper())        wheel_m = raw_input('Which ring-setting shall the M-rotor be set to? ')        if wheel_m.upper() in alphabet:            ring_setting_two = alphabet.index(wheel_m.upper())        wheel_l = raw_input('Which ring-setting shall the L-rotor be set to? ')        if wheel_l.upper() in alphabet:            ring_setting_three = alphabet.index(wheel_l.upper())                    return ring_setting_one, ring_setting_two, ring_setting_three# Introductiondef intro_enigma():    print 'Welcome to the Enigma emulator!'    print 'You will be asked to enter the Enigma-configuration, as well as the text you want encrypted'    while True:        answer = raw_input('Do you wish to continue or terminate the application? [continue/abort] ')        if answer.lower() == 'continue' or answer.lower() == 'c':            return True        elif answer.lower() == 'abort' or answer.lower() == 'a':            print 'Auf wiedersehen.'            sys.exit(1)        else:            print 'Please answer with \'continue\' or \'abort\'.'# Set the rotors to their start position# Based on the index settingdef set_to_start(start_index, rotor):    temp_rotor = Rotor(my_wheel = 1, my_setting = 0)    for i in range(len(rotor.my_rotor)):        if i + start_index < len(rotor.my_rotor):            temp_rotor.my_rotor[i] = rotor.my_rotor[i+start_index]        else:            temp_rotor.my_rotor[i] = rotor.my_rotor[(i+start_index) % len(rotor.my_rotor)]    rotor.my_rotor = temp_rotor.my_rotor    print rotor.my_rotor, 'final'    return rotor# Read the message to encryptdef read_message(rotor1, start_index_one, rotor2, start_index_two, rotor3, start_index_three, reflector):    message = raw_input('Type in the message you want encrypted: ')    # Remove all spaces    message = message.upper().strip().replace(' ', '')    encrypted_message = ''    notch_step_two = 0    notch_step_three = 0        # Get the notches    notch_one = rotor1.my_notch    notch_two = rotor2.my_notch    notch_three = rotor3.my_notch        # Check the index of the notch in the alphabet     alphabet = [chr(i) for i in range(65, 91)]    index_notch_one = alphabet.index(notch_one)    index_notch_two = alphabet.index(notch_two)    index_notch_three = alphabet. index(notch_three)    # Compare the notch index to the start position of the rotors    turn_notch_one = index_notch_one - start_index_one    if turn_notch_one < 0:        turn_notch_one += 26        print turn_notch_one, 'tnone'    turn_notch_two = index_notch_two - start_index_two    if turn_notch_two < 0:        turn_notch_two += 26    turn_notch_three = index_notch_three - start_index_three    if turn_notch_three < 0:        turn_notch_three += 26    #Check if the characters are only A to Z, answer again otherwise    for index in range(len(message)):            # Handle the notches.        turn_notch_one -= 1        if turn_notch_one < 0:            notch_step_two += 1 # To step the 2nd rotor            turn_notch_two -= 1            turn_notch_one = 25        if turn_notch_two == 0 and not turn_notch_one == 25:            if turn_notch_one == 24:                notch_step_three += 1 # To step the 3rd rotor                notch_step_two += 1                turn_notch_two = 25            else:                turn_notch_two = 25        # Call the encryption function        encrypted_message += get_encrypted_char(message[index], index, rotor1, rotor2, rotor3, reflector, start_index_one, start_index_two, start_index_three, notch_step_two, notch_step_three)        # Print string of 5 characters, separated by a space    parsed_message = ''    for i in range(len(encrypted_message)):        if not i % 4 == 0:            parsed_message += encrypted_message[i]        if i % 4 == 0:            parsed_message += ' ' + encrypted_message[i]    print 'The encrypted message is: ', parsed_message.strip()# Get the encrypted characterdef get_encrypted_char(letter, index, rotor1, rotor2, rotor3, reflector, start_index_one, start_index_two, start_index_three, notch_step_two, notch_step_three):    # 1st step: Let the 1st rotor rotate one more step than the index of the letter to be encrypted    offset = index + 1        # Check for wrap-around in case the new_index would not be one of the defined letters, ie between ACSCII 65 and 90    new_index = ord(letter) + offset    while new_index > 90 or new_index < 65:        if new_index > 90:            new_index = new_index - 91 + 65        elif new_index < 65:            new_index = new_index - 65 + 91    rotor1_in = rotor1.my_rotor[new_index-65][0]    rotor1_out = rotor1.my_rotor[new_index-65][1]    # 2nd step: Back the offset with the index for the middle rotor    new_index = ord(rotor1_out) - offset - start_index_one + start_index_two + notch_step_two    while new_index > 90 or new_index < 65:        if new_index > 90:            new_index = new_index - 91 + 65        elif new_index < 65:            new_index = new_index - 65 + 91    rotor2_in = chr(new_index)    for i in range(len(rotor2.my_rotor)):        if rotor2_in in rotor2.my_rotor[i]:            if rotor2.my_rotor[i][0] == rotor2_in:                rotor2_out = rotor2.my_rotor[i][1]                break        # 3rd step: Get the output for the 3rd, left, wheel    new_index = ord(rotor2_out) - start_index_two + start_index_three - notch_step_two + notch_step_three    while new_index > 90 or new_index < 65:        if new_index > 90:            new_index = new_index - 91 + 65        elif new_index < 65:            new_index = new_index - 65 + 91    rotor3_in = chr(new_index)    for i in range(len(rotor3.my_rotor)):        if rotor3_in in rotor3.my_rotor[i]:            if rotor3.my_rotor[i][0] == rotor3_in:                rotor3_out = rotor3.my_rotor[i][1]                break        # Step 4: Return the output from the Reflector    #reflector_in = rotor3_out    new_index = ord(rotor3_out) - start_index_three - notch_step_three    while new_index > 90 or new_index < 65:        if new_index > 90:            new_index = new_index - 91 + 65        elif new_index < 65:            new_index = new_index - 65 + 91    reflector_in = chr(new_index)    for i in range(len(reflector.my_rotor)):        if reflector_in in reflector.my_rotor[i]:            if reflector.my_rotor[i][0] == reflector_in:                reflector_out = reflector.my_rotor[i][1]                break        # Step 5: Go back, use the other side of the tuple    #rotor3_in = reflector_out    new_index = ord(reflector_out) + start_index_three + notch_step_three    while new_index > 90 or new_index < 65:        if new_index > 90:            new_index = new_index - 91 + 65        elif new_index < 65:            new_index = new_index - 65 + 91    rotor3_in = chr(new_index)    for i in range(len(rotor3.my_rotor)):        if rotor3_in in rotor3.my_rotor[i]:            if rotor3.my_rotor[i][1] == rotor3_in:                rotor3_out = rotor3.my_rotor[i][0]                break        # Step 6: Go through the middle rotor    new_index = ord(rotor3_out) - start_index_three + start_index_two + notch_step_two - notch_step_three    while new_index > 90 or new_index < 65:        if new_index > 90:            new_index = new_index - 91 + 65        elif new_index < 65:            new_index = new_index - 65 + 91    rotor2_in = chr(new_index)    for i in range(len(rotor2.my_rotor)):        if rotor2_in in rotor2.my_rotor[i]:            if rotor2.my_rotor[i][1] == rotor2_in:                rotor2_out = rotor2.my_rotor[i][0]                break        # Step 7: Get back the offset, see step 2 reversed    new_index = ord(rotor2_out) + offset + start_index_one - start_index_two - notch_step_two    while new_index > 90 or new_index < 65:        if new_index > 90:            new_index = new_index - 91 + 65        elif new_index < 65:            new_index = new_index - 65 + 91    rotor1_in = chr(new_index)    for i in range(len(rotor1.my_rotor)):        if rotor1_in in rotor1.my_rotor[i]:            if rotor1.my_rotor[i][1] == rotor1_in:                rotor1_out = rotor1.my_rotor[i][0]                break        # Step 8: Reverse step 1 to get the final letter    new_index = ord(rotor1_out) - offset - start_index_one    #new_index = ord(rotor1_out) - letter_index    while new_index > 90 or new_index < 65:        if new_index > 90:            new_index = new_index - 91 + 65        elif new_index < 65:            new_index = new_index - 65 + 91    letter = chr(new_index)    return letter# Main functiondef main():    if intro_enigma(): # If the user wants to proceed        # Get the rotor setup        pos_rotor_one, pos_rotor_two, pos_rotor_three, pos_reflector = get_rotor_setup()                # Get the ring settings (internal wiring) from the user        ring_setting_one, ring_setting_two, ring_setting_three = get_ring_setting_index()        # Create the wheels, with regards to the ring settings        rotor1 = Rotor(my_wheel = pos_rotor_one, my_setting = ring_setting_one)        rotor2 = Rotor(my_wheel = pos_rotor_two, my_setting = ring_setting_two)        rotor3 = Rotor(my_wheel = pos_rotor_three, my_setting = ring_setting_three)        reflector = Rotor(my_wheel = pos_reflector, my_setting = 0)                # Get the start configuration (ring start index) from the user        start_index_one, start_index_two, start_index_three = get_start_index()                # Set the wheels to their start position        rotor1 = set_to_start(start_index_one, rotor1)        rotor2 = set_to_start(start_index_two, rotor2)        rotor3 = set_to_start(start_index_three, rotor3)                # Read in the message        read_message(rotor1, start_index_one, rotor2, start_index_two, rotor3, start_index_three, reflector)# Init functionif __name__ == '__main__':    main()