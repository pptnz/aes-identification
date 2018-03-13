import tensorflow as tf
import numpy as np
import os
from input_data import train_data, train_labels, validation_data, validation_labels, test_data, test_labels
from input_tensor import input_tensor
from answer_tensor import answer_tensor
from settings import Settings
from global_step import global_step
from train_step import train_step
from keep_prob import keep_prob
from loss import loss
from import_neural_net import import_neural_net
from csv_writer import CSVWriter
from sample_with_probability import sample_with_probability
from progress_bar import progress_bar
from timer import Timer

settings = Settings("./settings.json")
max_global_step = settings.read("step_info", "global_step")
save_step = settings.read("step_info", "save_step")
validation_step = settings.read("step_info", "validation_step")
loss_step = settings.read("step_info", "loss_step")
batch_size = settings.read("hyperparameters", "batch_size")
keep_prob_value = settings.read("hyperparameters", "keep_prob")
num_validation_files = settings.read("validation_data", "end") - settings.read("validation_data", "begin") + 1
num_test_files = settings.read("test_data", "end") - settings.read("test_data", "begin") + 1
num_groups = settings.read("data_info", "num_groups")
neural_net_name = settings.read("neural_net_info", "neural_net_name")
neural_net = import_neural_net(neural_net_name)
decision_threshold = settings.read("decision_info", "threshold")
validation_batch_size = settings.read("test_info", "validation_batch_size")
test_batch_size = settings.read("test_info", "test_batch_size")
sampling_enabled = settings.read("debugging", "sampling")
true_positive_sampling_rate = settings.read("debugging", "sampling_prob", "true_positive")
true_negative_sampling_rate = settings.read("debugging", "sampling_prob", "true_negative")
false_positive_sampling_rate = settings.read("debugging", "sampling_prob", "false_positive")
false_negative_sampling_rate = settings.read("debugging", "sampling_prob", "false_negative")

model_save_path = "./saved_model/{}/".format(neural_net_name)
model_file_save_path = model_save_path + "{}.ckpt".format(neural_net_name)

if not os.path.exists(model_save_path):
    os.makedirs(model_save_path)

with tf.Session() as sess:
    sess.run(tf.local_variables_initializer())
    sess.run(tf.global_variables_initializer())

    saver = tf.train.Saver()

    latest_checkpoint_path = tf.train.latest_checkpoint(model_save_path)
    if latest_checkpoint_path is not None:
        print("Saved model is found. Do you want to restore that model? (Y/n) : ", end="")
        user_input = input()
        if user_input.strip().lower() == "n":
            print("New model is initialized.")
        else:
            print("Restoring model...")
            saver.restore(sess, latest_checkpoint_path)
            print("Model successfully restored.")
    else:
        print("No saved model is found. New model is successfully initialized.")

    coord = tf.train.Coordinator()
    threads = tf.train.start_queue_runners(coord=coord)

    timer = Timer()

    test_true_negative_writer = CSVWriter("true_negative.csv", directory="./test_sampled_fragments")
    test_true_positive_writer = CSVWriter("true_positive.csv", directory="./test_sampled_fragments")
    test_false_positive_writer = CSVWriter("false_positive.csv", directory="./test_sampled_fragments")
    test_false_negative_writer = CSVWriter("false_negative.csv", directory="./test_sampled_fragments")

    while True:
        data, labels = sess.run([train_data, train_labels])
        sess.run(train_step, feed_dict={input_tensor: data, answer_tensor: labels, keep_prob: keep_prob_value})

        global_step_value = tf.train.global_step(sess, global_step)
        progress_bar(global_step_value, max_global_step)

        if global_step_value % loss_step == 0:
            data, labels = sess.run([train_data, train_labels])
            print("At Step {}, Loss: {}".format(
                global_step_value,
                sess.run(loss, feed_dict={input_tensor: data, answer_tensor: labels, keep_prob: 1.0})))

        if global_step_value % save_step == 0:
            print("\nSaving...")
            saver.save(sess, model_file_save_path, global_step=global_step_value)
            print("Model Successfully Saved.\n")
            pass

        if global_step_value % validation_step == 0:
            print("\nValidating...")
            accuracy_table = [[0 for _ in range(num_groups)] for _ in range(num_groups)]
            max_validation_step = int(num_validation_files / validation_batch_size)
            for step in range(1, max_validation_step + 1):
                data, labels = sess.run([validation_data, validation_labels])

                timer.start()
                prediction_value = sess.run(neural_net.output_tensor, feed_dict={input_tensor: data, keep_prob: 1.0})
                timer.stop()

                answer_value = labels

                for pred, ans in zip(prediction_value, answer_value):
                    answer_group = np.argmax(ans)
                    if pred[1] >= decision_threshold:
                        pred_group = 1
                    else:
                        pred_group = 0
                    accuracy_table[answer_group][pred_group] += 1

                progress_bar(step, max_validation_step)

            print("\nValidation Result")
            print("Percentage:")
            for row in accuracy_table:
                for col in row / np.sum(row) * 100:
                    print("{:>6.2f}%\t".format(col), end="")
                print()
            print("\nCount:")
            for row in accuracy_table:
                for col in row:
                    print("{:>8}\t".format(col), end="")
                print()

            correct_count = 0
            for i in range(num_groups):
                correct_count += accuracy_table[i][i]
            print("Accuracy: {:>6.2f}%\n".format(correct_count / num_validation_files * 100))

            print("Elapsed Time: {:>6.5f} sec in total, {:.2e} sec/fragment\n"
                  .format(timer.time(), timer.time() / num_validation_files))

            timer.reset()

        if global_step_value >= max_global_step:
            break

    print("\nTesting...")

    accuracy_table = [[0 for _ in range(num_groups)] for _ in range(num_groups)]
    max_test_step = int(num_test_files / test_batch_size)
    for step in range(1, max_test_step + 1):
        data, labels = sess.run([test_data, test_labels])

        timer.start()
        prediction_value = sess.run(neural_net.output_tensor, feed_dict={input_tensor: data, keep_prob: 1.0})
        timer.stop()

        answer_value = labels

        index_in_batch = 0
        for pred, ans in zip(prediction_value, answer_value):
            answer_group = np.argmax(ans)
            if pred[1] >= decision_threshold:
                pred_group = 1
            else:
                pred_group = 0
            accuracy_table[answer_group][pred_group] += 1

            if sampling_enabled:
                data_sample = data.tolist()[index_in_batch]
                data_histogram = np.bincount(data_sample, minlength=256).tolist()
                data_std = [np.std(data_histogram)]
                data_to_write = [data_sample, data_histogram, data_std]

                if answer_group == 0 and pred_group == 0:
                    # True Negative
                    if sample_with_probability(true_negative_sampling_rate):
                        test_true_negative_writer.write(data_to_write)
                elif answer_group == 1 and pred_group == 1:
                    # True Positive
                    if sample_with_probability(true_positive_sampling_rate):
                        test_true_positive_writer.write(data_to_write)
                elif answer_group == 0 and pred_group == 1:
                    # False Positive
                    if sample_with_probability(false_positive_sampling_rate):
                        test_false_positive_writer.write(data_to_write)
                else:
                    # False Negative
                    if sample_with_probability(false_negative_sampling_rate):
                        test_false_negative_writer.write(data_to_write)

            index_in_batch += 1

        progress_bar(step, max_test_step)

    print("\nTesting Result")
    print("Percentage:")
    for row in accuracy_table:
        for col in row / np.sum(row) * 100:
            print("{:>6.2f}%\t".format(col), end="")
        print()
    print("\nCount:")
    for row in accuracy_table:
        for col in row:
            print("{:>8}\t".format(col), end="")
        print()

    correct_count = 0
    for i in range(num_groups):
        correct_count += accuracy_table[i][i]
    print("Accuracy: {:>6.2f}%\n".format(correct_count / num_test_files * 100))

    print("Elapsed Time: {:>6.5f} sec in total, {:.2e} sec/fragment\n"
          .format(timer.time(), timer.time() / num_test_files))

    timer.reset()

    coord.request_stop()
    coord.join(threads)
