import matplotlib.pyplot as plt

class RoundRobinScheduler:
    def __init__(self, quantum_time, context_switch_time):
        # Initialize the scheduler with quantum time and context switch time
        self.quantum_time = quantum_time
        self.context_switch_time = context_switch_time
        self.process_control_blocks = []
        self.working_processes = []
        self.counter = 0
        self.ready_queue = []
        self.waiting_queue = []
        self.added_processes = []
        self.execution_chart = []

    def get_input(self):
        # Get user input for number of processes and their attributes
        num_processes = int(input('Enter number of processes: '))
        for i in range(num_processes):
            process_name = input('Enter process name: ')
            self.process_control_blocks.append({
                'process_id': process_name,
                'arrival_time': int(input('Enter arrival time of ' + process_name + ': ')),
                'burst_time': int(input('Enter burst time of ' + process_name + ': ')),
                'waiting_time': 0,
                'turnaround_time': 0,
                'completion_time': 0,
            })

    def increment_counter(self):
        # Increment the global counter
        self.counter += 1
        # Check for processes to be executed
        self.check_for_processes()

    def check_for_processes(self):
        # Check if all processes are executed
        if len(self.process_control_blocks) == len(self.added_processes):
            if self.working_processes == [] and self.waiting_queue == []:
                return

        # Check for processes eligible for execution
        for i, process in enumerate(self.process_control_blocks):
            if self.counter >= process['arrival_time']:
                if process['process_id'] not in self.added_processes:
                    self.working_processes.append(process.copy())
                    self.added_processes.append(process['process_id'])

        if len(self.working_processes) > 0:
            # Move the process to execution
            self.move_to_processing(self.working_processes[0])
        elif len(self.waiting_queue) > 0:
            # Move the process from waiting queue to execution
            self.working_processes.append(self.waiting_queue[0])
            self.waiting_queue.pop(0)
            self.move_to_processing(self.working_processes[0])
        else:
            # If no process to execute, increment counter
            self.increment_counter()

    def sort_processes_by_arrival_time(self, processes):
        # Sort the processes by arrival time
        processes.sort(key=lambda x: x['arrival_time'])

    def move_to_processing(self, process):
        # Move the process to processing state
        if len(self.ready_queue) != 0 and self.ready_queue[-1] != process['process_id']:
            self.counter += self.context_switch_time

        self.ready_queue.append(process['process_id'])
        temp = [int(process['process_id'])]

        if process['burst_time'] <= self.quantum_time:
            # If burst time is less than quantum time
            temp.append(self.counter)
            self.counter += process['burst_time']
            temp.append(self.counter)
            process['burst_time'] = 0
            self.working_processes.pop(0)
            for i, pcb in enumerate(self.process_control_blocks):
                if pcb['process_id'] == process['process_id']:
                    self.process_control_blocks[i]['completion_time'] = self.counter
                    self.process_control_blocks[i]['turnaround_time'] = self.process_control_blocks[i]['completion_time'] - self.process_control_blocks[i]['arrival_time']
                    self.process_control_blocks[i]['waiting_time'] = self.process_control_blocks[i]['turnaround_time'] - self.process_control_blocks[i]['burst_time']

            if len(self.waiting_queue) >= 1:
                self.working_processes.append(self.waiting_queue[0])
                self.waiting_queue.pop(0)
                self.check_for_processes()
            else:
                self.check_for_processes()

        else:
            # If burst time is greater than quantum time
            temp.append(self.counter)
            self.counter += self.quantum_time
            temp.append(self.counter)
            process['burst_time'] -= self.quantum_time
            self.waiting_queue.append(process)
            self.working_processes.pop(0)

            if len(self.waiting_queue) > 1:
                self.working_processes.append(self.waiting_queue[0])
                self.waiting_queue.pop(0)
                self.check_for_processes()
            else:
                self.check_for_processes()

        self.execution_chart.append(temp)

    def get_avg_times(self):
        # Calculate and print average waiting and turnaround times
        wait_avg = sum(process['waiting_time'] for process in self.process_control_blocks) / len(self.process_control_blocks)
        turnaround_avg = sum(process['turnaround_time'] for process in self.process_control_blocks) / len(self.process_control_blocks)
        print('Average waiting time: {:.2f}'.format(wait_avg))
        print('Average turnaround time: {:.2f}'.format(turnaround_avg))

    def print_data(self):
        # Print process data
        print('{:^20}{:^20}{:^20}{:^20}{:^20}{:^20}'.format('Process', 'Arrival Time', 'Burst Time', 'Waiting Time', 'Turnaround Time', 'Completion Time'))
        for pcb in self.process_control_blocks:
            print('{:^20}{:^20}{:^20}{:^20}{:^20}{:^20}'.format(pcb['process_id'], pcb['arrival_time'], pcb['burst_time'], pcb['waiting_time'], pcb['turnaround_time'], pcb['completion_time']))

    def plot_execution_chart(self):
        # Plot execution chart
        self.execution_chart.reverse()
        plt.xticks(range(0, self.counter + 1))
        plt.yticks(range(0, len(self.process_control_blocks) + 1))
        plt.gca().invert_yaxis()

        for i in range(len(self.execution_chart)):
            x = []
            y = []
            for j in range(self.execution_chart[i][2] - self.execution_chart[i][1] + 1):
                x.append(j + self.execution_chart[i][1])
                y.append(self.execution_chart[i][0])
            plt.plot(x, y, color='purple', linewidth=10)

        plt.show()

    def run(self):
        # Execute the scheduler
        self.get_input()
        self.check_for_processes()
        self.print_data()
        self.get_avg_times()
        self.plot_execution_chart()

quantum_time = int(input('Enter the quantum time: '))
context_switch_time = int(input('Enter the context switch time: '))

scheduler = RoundRobinScheduler(quantum_time, context_switch_time)
scheduler.run()
