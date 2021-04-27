index = 1;
for ep = 1:epohs
    training_data_file = fopen("mnist_dataset/mnist_train.csv");
    next = fgetl(training_data_file);
    while next ~= -1
        disp(ep+":"+index);
        index=index+1;
        all_values = str2num(char(strsplit(strrep(next, ',', ' '),',')));
        array = all_values(2:end).';
        targets = zeros(output_nodes, 1)+0.01;
        targets(all_values(1)+1) = 0.99;
        inputs = (array./255)*0.99+0.01;
        n.train(inputs, targets);
        next = fgetl(training_data_file);
    end
    fclose(training_data_file);
end