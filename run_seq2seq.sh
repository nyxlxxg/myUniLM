python run_seq2seq.py \
  --data_dir "/workspace/nlp/nyg/unilm/data"  \
  --src_file train.csv \
  --model_type unilm  \
  --model_name_or_path "/workspace/model/pretrain/Unilm" \
  --output_dir "./output/" \
  --max_seq_length 1024  \
  --max_position_embeddings 512  \
  --do_train \
  --do_lower_case \
  --train_batch_size 32 \
  --learning_rate 1e-5 \
  --num_train_epochs 5

# local
#  --data_dir "/Users/ningyuguang/data/summary"
#  --src_file drama.json
#  --model_type unilm
#  --model_name_or_path "/Users/ningyuguang/Model/torch_unilm_model"
#  --output_dir "/Users/ningyuguang/Work/myUniLM/output/"
#  --max_seq_length 1024
#  --max_position_embeddings 512
#  --do_train
#  --do_lower_case
#  --train_batch_size 4
#  --learning_rate 1e-5
#  --num_train_epochs 5