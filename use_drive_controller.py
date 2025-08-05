


from use_servos import stop, forward, backward, left, right, forward_step, backward_step, left_step, right_step
import time


class drive_controller:
    def __init__(self):
        self.current_movement = None
    
    
    def stop(self):
        self.current_movement = None
        stop()
        
    def forward(self):
        self.current_movement = "forward"
        forward()
    
    def forward_step(self,t=0.25):
        self.current_movement = "forward"
        forward_step(t)
        self.stop()
    
    def backward(self):
        self.current_movement = "backward"
        backward()
    
    def backward_step(self,t=0.25):
        self.current_movement = "backward"
        backward_step(t)
        self.stop()
    
    def left(self):
        self.current_movement = "left"
        left()
    
    def left_step(self,t=0.25):
        self.current_movement = "left"
        left_step(t)
        self.stop()
    
    def right(self):
        self.current_movement = "right"
        right()
    
    def right_step(self,t=0.25):
        self.current_movement = "right"
        right_step(t)
        self.stop()


        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
        
