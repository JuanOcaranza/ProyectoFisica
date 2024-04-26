class Unit_converter:
    def __init__(self,
                 current_distance, target_distance,
                 current_time, target_time,
                 current_angle = 1, target_angle = 1
                 ):
        self.distance_factor = target_distance / current_distance
        self.time_factor = target_time / current_time
        self.angle_factor = target_angle / current_angle

    def convert_position(self, df, columns):
        for column in columns:
            df[column] = df[column] * self.distance_factor
        
        return df
    
    def convert_velocity(self, df, columns):
        for column in columns:
            df[column] = df[column] * self.distance_factor / self.time_factor
        
        return df
    
    def convert_acceleration(self, df, columns):
        for column in columns:
            df[column] = df[column] * self.distance_factor / (self.time_factor ** 2)
        
        return df
    
    def convert_time(self, df, columns):
        for column in columns:
            df[column] = df[column] * self.time_factor
        
        return df
    
    def convert_angle(self, df, columns):
        for column in columns:
            df[column] = df[column] * self.angle_factor
        
        return df
    
    def convert_angular_velocity(self, df, columns):
        for column in columns:
            df[column] = df[column] * self.angle_factor / self.time_factor
        
        return df