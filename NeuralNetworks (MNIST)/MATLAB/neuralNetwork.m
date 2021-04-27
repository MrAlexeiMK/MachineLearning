classdef neuralNetwork < handle
    properties
        inodes
        hnodes
        onodes
        lr
        wih
        who
    end
    methods
        function obj = neuralNetwork(varargin)
            obj.inodes = varargin{1};
            obj.hnodes = varargin{2};
            obj.onodes = varargin{3};
            obj.lr = varargin{4};
            
            obj.wih = obj.hnodes^-0.5*(2*rand(obj.hnodes, obj.inodes)-1);
            obj.who = obj.onodes^-0.5*(2*rand(obj.onodes, obj.hnodes)-1);
        end
        
        function train(obj, varargin)
            inputs_list = varargin{1};
            targets_list = varargin{2};
            hidden_inputs = obj.wih*inputs_list;
            hidden_outputs = activation_function(hidden_inputs);
            final_inputs = obj.who*hidden_outputs;
            final_outputs = activation_function(final_inputs);
            
            output_errors = targets_list-final_outputs;
            hidden_errors = obj.who.'*output_errors;
            
            
            
            obj.who = obj.who + obj.lr .* ((output_errors .* final_outputs .* (1 - final_outputs)) .* hidden_outputs.');
            obj.wih = obj.wih + obj.lr .* ((hidden_errors .* hidden_outputs .* (1 - hidden_outputs)) .* inputs_list.');
        end
        
        function final_outputs = query(obj, varargin)
            inputs_list = varargin{1};
            hidden_inputs = obj.wih*inputs_list;
            hidden_outputs = activation_function(hidden_inputs);
            final_inputs = obj.who*hidden_outputs; 
            final_outputs = activation_function(final_inputs);
        end
        
        function saveW(obj)
            dlmwrite('weights/wih', obj.wih);
            dlmwrite('weights/who', obj.who);
        end
        
        function loadW(obj)
            obj.wih = dlmread('weights/wih');
            obj.who = dlmread('weights/who');
        end
    end
end

