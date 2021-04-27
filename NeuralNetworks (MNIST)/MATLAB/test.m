test_data_file = fopen("mnist_dataset/mnist_test.csv");
next = fgetl(test_data_file);
scor = 0;
numbers = 0;
while next ~= -1
    all_values = str2num(char(strsplit(strrep(next, ',', ' '),',')));
    array = all_values(2:end).';
    inputs = (array./255)*0.99+0.01;
    correct = all_values(1);
    outputs = n.query(inputs);
    [value, label] = max(outputs);
    if label-1 == correct
        scor=scor+1;
    end
    numbers=numbers+1;
    %disp(correct+":"+(label-1));
    next = fgetl(test_data_file);
end
fclose(test_data_file);
disp((scor/numbers)*100+"%");