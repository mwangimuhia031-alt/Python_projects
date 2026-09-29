def hanoi_solver(n):
    # Initialize the three rods
    rods = {
        'A': list(range(n, 0, -1)),
        'B': [],
        'C': []
    }
    
    moves = []

    def record_state():
        # Record the current state formatted as [A] [B] [C]
        moves.append(f"{rods['A']} {rods['B']} {rods['C']}")

    # Record initial starting arrangement
    record_state()

    def solve(disks, source, target, auxiliary):
        if disks == 1:
            rods[target].append(rods[source].pop())
            record_state()
            return
        
        # Move n-1 disks from source to auxiliary
        solve(disks - 1, source, auxiliary, target)
        
        # Move the nth disk from source to target
        rods[target].append(rods[source].pop())
        record_state()
        
        # Move n-1 disks from auxiliary to target
        solve(disks - 1, auxiliary, target, source)

    solve(n, 'A', 'C', 'B')
    return '\n'.join(moves)