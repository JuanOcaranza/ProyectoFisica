class Unit_converter:
    def __init__(self, current_distance, target_distance, current_time, target_time):
        self.distance_factor = target_distance / current_distance
        self.time_factor = target_time / current_time

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