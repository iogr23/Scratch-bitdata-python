import cv2
import numpy as np

# Define the lookup table for 6-bit binary to characters (a-z, 0-9, special characters)
lookup_table = {
    '000000': 'a', '000001': 'b', '000010': 'c', '000011': 'd', '000100': 'e',
    '000101': 'f', '000110': 'g', '000111': 'h', '001000': 'i', '001001': 'j',
    '001010': 'k', '001011': 'l', '001100': 'm', '001101': 'n', '001110': 'o',
    '001111': 'p', '010000': 'q', '010001': 'r', '010010': 's', '010011': 't',
    '010100': 'u', '010101': 'v', '010110': 'w', '010111': 'x', '011000': 'y',
    '011001': 'z', '011010': '0', '011011': '1', '011100': '2', '011101': '3',
    '011110': '4', '011111': '5', '100000': '6', '100001': '7', '100010': '8',
    '100011': '9', '100100': '!', '100101': '@', '100110': '#', '100111': '$',
    '101000': '%', '101001': '^', '101010': '&', '101011': '*', '101100': '(',
    '101101': ')', '101110': '-', '101111': '_', '110000': '+', '110001': '=',
    '110010': '[', '110011': ']', '110100': '{', '110101': '}', '110110': '|',
    '110111': ':', '111000': ';', '111001': "'", '111010': '"', '111011': '<',
    '111100': '>', '111101': ',', '111110': '.', '111111': '?'
}

def binary_frame(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # Convert to binary: 1 for white, 0 for black
    _, binary = cv2.threshold(gray_frame, 127, 1, cv2.THRESH_BINARY)
    
    # Flatten the binary frame into a 1D array
    binary = binary.flatten()  # Flatten to 1D array
    padded_length = (len(binary) + 7) // 8 * 8  # Pad length to be divisible by 8
    binary_padded = np.pad(binary, (0, padded_length - len(binary)), 'constant', constant_values=0)
    
    # Convert the entire binary array to a single binary string
    binary_string = ''.join(str(bit) for bit in binary_padded)
    
    # Split the binary string into chunks of 6 bits
    compressed_output = []
    for i in range(0, len(binary_string), 6):
        chunk = binary_string[i:i+6]
        if len(chunk) < 6:
            # Pad with zeros if the chunk is less than 6 bits
            chunk = chunk.ljust(6, '0')
        
        # Map the 6-bit chunk to a character using the lookup table
        compressed_output.append(lookup_table[chunk])
    
    return ''.join(compressed_output)  # Return the compressed string

def process_video(input_file, output_file):
    # Open the output file in 'w' mode to clear its contents
    with open(output_file, 'w') as f:
        pass  # Just open and close to truncate the file

    # Open the video file
    cap = cv2.VideoCapture(input_file)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    frame_count = 0

    # Process each frame
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize the frame to 480x360
        frame = cv2.resize(frame, (480, 360))

        compressed_string = binary_frame(frame)
        
        # Write the compressed string directly to the output file in 'a' mode (append)
        with open(output_file, 'a') as f:  # Write in text mode
            f.write(compressed_string + '\n')  # Write the compressed string for the frame
            
        frame_count += 1
        if frame_count % 50 == 0:
            print(f"{frame_count} Frames processed")

    cap.release()
    print(f"Total frames processed: {frame_count}. Compressed strings written to {output_file}")

if __name__ == "__main__":
    input_file = input("Enter the path to the MP4 video file: ")
    output_file = input("Enter the path for the output TXT file: ")
    process_video(input_file, output_file)
