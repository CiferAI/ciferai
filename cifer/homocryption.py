from lightphe import LightPHE

class HomomorphicEncryption:
    def __init__(self, algorithm_name="Paillier"):
        # Generate private-public key pair
        self.cs = LightPHE(algorithm_name=algorithm_name)
        self.cs.export_keys(target_file="public.txt", public=True)
        self.cs.export_keys(target_file="private.txt", public=False)

    def encrypt(self, message):
        """Encryption function"""
        return self.cs.encrypt(message)

    def decrypt(self, ciphertext):
        """Decryption function"""
        return self.cs.decrypt(ciphertext)

# Example usage
if __name__ == "__main__":
    # Create Homomorphic object
    homomorphic_encryption = HomomorphicEncryption()

    # Set plaintext message
    m1 = 17
    m2 = 23

    # Encrypt message
    c1 = homomorphic_encryption.encrypt(m1)
    c2 = homomorphic_encryption.encrypt(m2)

    print("Ciphertext 1:", c1.value)  # Display ciphertext
    print("Ciphertext 2:", c2.value)  # Display ciphertext

    # Decrypt message
    dec_m1 = homomorphic_encryption.decrypt(c1)
    dec_m2 = homomorphic_encryption.decrypt(c2)

    print("Decrypted message 1:", dec_m1)  # Should display 17
    print("Decrypted message 2:", dec_m2)  # Should display 23
