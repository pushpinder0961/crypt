import hashlib
import time
import uuid

class TicketBlock:
    def __init__(self, index, timestamp, ticket_id, buyer_name, event_name, previous_hash):
        self.index = index
        self.timestamp = timestamp
        self.ticket_id = ticket_id
        self.buyer_name = buyer_name
        self.event_name = event_name
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.ticket_id}{self.buyer_name}{self.event_name}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class TicketBlockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return TicketBlock(0, time.time(), "GENESIS", "System", "Genesis Event", "0")

    def get_latest_block(self):
        return self.chain[-1]

    def issue_ticket(self, buyer_name, event_name):
        ticket_id = str(uuid.uuid4())  # Unique ticket ID
        previous_block = self.get_latest_block()
        new_block = TicketBlock(
            index=previous_block.index + 1,
            timestamp=time.time(),
            ticket_id=ticket_id,
            buyer_name=buyer_name,
            event_name=event_name,
            previous_hash=previous_block.hash
        )
        self.chain.append(new_block)
        return ticket_id

    def verify_ticket(self, ticket_id):
        for block in self.chain:
            if block.ticket_id == ticket_id:
                return block
        return None

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i-1]
            if current.hash != current.calculate_hash():
                return False
            if current.previous_hash != previous.hash:
                return False
        return True

    def show_all_tickets(self):
        for block in self.chain[1:]:  # Skip genesis block
            print(f"Index: {block.index}")
            print(f"Ticket ID: {block.ticket_id}")
            print(f"Buyer: {block.buyer_name}")
            print(f"Event: {block.event_name}")
            print(f"Issued on: {time.ctime(block.timestamp)}")
            print(f"Hash: {block.hash}")
            print("-" * 50)

if __name__ == "__main__":
    system = TicketBlockchain()

    while True:
        print("\n🎟️ Blockchain Ticketing System 🎟️")
        print("1. Issue New Ticket")
        print("2. Verify Ticket")
        print("3. Show All Issued Tickets")
        print("4. Validate Blockchain Integrity")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == "1":
            buyer = input("Enter buyer name: ")
            event = input("Enter event name: ")
            ticket = system.issue_ticket(buyer, event)
            print(f"✅ Ticket issued successfully! Ticket ID: {ticket}")

        elif choice == "2":
            tid = input("Enter ticket ID to verify: ")
            result = system.verify_ticket(tid)
            if result:
                print("✅ Ticket is VALID!")
                print(f"Buyer: {result.buyer_name}, Event: {result.event_name}, Issued: {time.ctime(result.timestamp)}")
            else:
                print("❌ Ticket is INVALID or not found.")

        elif choice == "3":
            system.show_all_tickets()

        elif choice == "4":
            valid = system.is_chain_valid()
            if valid:
                print("✅ Blockchain is valid. No tampering detected.")
            else:
                print("❌ Blockchain integrity failed. Tampering detected!")

        elif choice == "5":
            print("👋 Exiting...")
            break

        else:
            print("❗ Invalid option. Try again.")
