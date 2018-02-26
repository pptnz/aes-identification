import tensorflow as tf
import numpy as np
import os
import time
from input_data import train_data, train_labels, validation_data, validation_labels, test_data, test_labels
from input_tensor import input_tensor
from answer_tensor import answer_tensor
from settings import Settings
from global_step import global_step
from train_step import train_step
from keep_prob import keep_prob
from loss import loss
from import_neural_net import import_neural_net
from progress_bar import progress_bar

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
            validation_start_time = time.time()
            accuracy_table = [[0 for _ in range(num_groups)] for _ in range(num_groups)]
            max_validation_step = int(num_validation_files / validation_batch_size)
            for step in range(1, max_validation_step + 1):
                data, labels = sess.run([validation_data, validation_labels])
                prediction_value = sess.run(neural_net.output_tensor, feed_dict={input_tensor: data, keep_prob: 1.0})
                answer_value = labels

                for pred, ans in zip(prediction_value, answer_value):
                    answer_group = np.argmax(ans)
                    if pred[1] >= decision_threshold:
                        pred_group = 1
                    else:
                        pred_group = 0
                    accuracy_table[answer_group][pred_group] += 1

                progress_bar(step, max_validation_step)
            validation_end_time = time.time()

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

            elapsed_time = validation_end_time - validation_start_time
            print("Elapsed Time: {:>6.5f} sec in total, {:.2e} sec/fragment\n"
                  .format(elapsed_time, elapsed_time / num_validation_files))

        if global_step_value >= max_global_step:
            break

    print("\nTesting...")
    test_start_time = time.time()
    accuracy_table = [[0 for _ in range(num_groups)] for _ in range(num_groups)]
    max_test_step = int(num_test_files / test_batch_size)
    for step in range(1, max_test_step + 1):
        data, labels = sess.run([test_data, test_labels])
        prediction_value = sess.run(neural_net.output_tensor,
                                    feed_dict={input_tensor: data, keep_prob: 1.0})
        answer_value = labels

        for pred, ans in zip(prediction_value, answer_value):
            answer_group = np.argmax(ans)
            if pred[1] >= decision_threshold:
                pred_group = 1
            else:
                pred_group = 0
            accuracy_table[answer_group][pred_group] += 1

        progress_bar(step, max_test_step)
    test_end_time = time.time()

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

    elapsed_time = test_end_time - test_start_time
    print("Elapsed Time: {:>6.5f} sec in total, {:.2e} sec/fragment\n"
          .format(elapsed_time, elapsed_time / num_validation_files))

    coord.request_stop()
    coord.join(threads)