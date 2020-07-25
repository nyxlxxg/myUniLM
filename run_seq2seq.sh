nohup python3 -u run_seq2seq.py --data_dir /data/unilm/data_file/ --src_file train_data.json --model_type unilm --model_name_or_path /data/unilm/yunwen_unilm/ --output_dir /data/unilm/output_dir/ --max_seq_length 512 --max_position_embeddings 512 --do_train --do_lower_case --train_batch_size 32 --learning_rate 1e-5 --num_train_epochs 3 > log.log 2>&1 &