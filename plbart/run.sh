#!/usr/bin/env bash
#check save dir

export PYTHONIOENCODING=utf-8;
CURRENT_DIR=`pwd`
CODE_DIR_HOME=`realpath ..`;
export PYTHONPATH=$CODE_DIR_HOME;

evaluator_script="${CODE_DIR_HOME}/evaluation";
codebleu_path="${CODE_DIR_HOME}/evaluation/CodeBLEU";
TEST_CASES="../data/atcoder_test_cases";

GPU=${1:-0};
SOURCE=${2:-python};
TARGET=${3:-python};
DATA_SRC=${4:-codenet};
WITH_VERDICT=${5:-false};

export CUDA_VISIBLE_DEVICES=$GPU
echo "Source: $SOURCE Target: $TARGET"

if [[ $WITH_VERDICT == 'false' ]]; then
    path_2_data=${CODE_DIR_HOME}/data/${SOURCE}/processed;#with_verdict
    SAVE_DIR=${CURRENT_DIR}/${DATA_SRC}/${SOURCE}2${TARGET};#_with_verdict

else
    path_2_data=${CODE_DIR_HOME}/data/${SOURCE}/processed_with_verdict
    SAVE_DIR=${CURRENT_DIR}/${DATA_SRC}/${SOURCE}2${TARGET}_with_verdict;#_with_verdict

fi

CACHE_DIR=${SAVE_DIR}/cached_data
mkdir -p $SAVE_DIR
mkdir -p $CACHE_DIR

#pretrained_model=${CODE_DIR_HOME}/models/codet5_base;

pretrained_model=${SAVE_DIR}/checkpoint-best-ppl;

tokenizer_path=${CURRENT_DIR}/bpe;
source_length=510;
target_length=510;


function train () {

NUM_TRAIN_EPOCHS=20; #20
lr=5e-5;
TRAIN_BATCH_SIZE=4; # per_gpu_train_bsz * num_gpu 
GRAD_ACCUM_STEP=8; # effective_bsz = train_bsz * grad_accum_steps

python run_gen.py \
    --do_train \
    --do_eval \
    --save_last_checkpoints \
    --always_save_model \
    --task translate \
    --sub_task "${SOURCE}-${TARGET}" \
    --model_type codet5 \
    --tokenizer_name roberta-base \
    --tokenizer_path $tokenizer_path \
    --output_dir $SAVE_DIR \
    --num_train_epochs $NUM_TRAIN_EPOCHS \
    --warmup_steps 100 \
    --learning_rate $lr \
    --patience 2 \
    --data_dir $path_2_data \
    --cache_path $CACHE_DIR \
    --res_dir $SAVE_DIR \
    --train_batch_size $TRAIN_BATCH_SIZE \
    --gradient_accumulation_steps $GRAD_ACCUM_STEP \
    --eval_batch_size 8 \
    --max_source_length $source_length \
    --max_target_length $target_length \
    --beam_size 5 \
    --data_num -1 \
    2>&1 | tee ${SAVE_DIR}/training.log;

}


function evaluate () {

MODEL_PATH=${SAVE_DIR}/checkpoint-best-ppl/pytorch_model.bin;
RESULT_FILE=${SAVE_DIR}/result.txt;
GOUND_TRUTH_PATH=${path_2_data}/test.jsonl;


python run_gen.py \
    --do_test \
    --model_type codet5 \
    --tokenizer_name roberta-base \
    --tokenizer_path $tokenizer_path \
    --model_name_or_path $pretrained_model \
    --task translate \
    --sub_task "${SOURCE}-${TARGET}" \
    --output_dir $SAVE_DIR \
    --data_dir $path_2_data \
    --cache_path $CACHE_DIR \
    --res_dir $SAVE_DIR \
    --eval_batch_size 8 \
    --max_source_length $source_length \
    --max_target_length $target_length \
    --beam_size 5 \
    --data_num -1 \
    2>&1 | tee ${SAVE_DIR}/evaluation.log;

echo "Evaluating Bleu" 
python $evaluator_script/evaluator.py \
    --references $GOUND_TRUTH_PATH \
    --predictions $SAVE_DIR/test.output \
    --language $TARGET \
    2>&1 | tee $RESULT_FILE;
echo "Evaluating CodeBleu"
cd $codebleu_path;
python calc_code_bleu.py \
    --ref $GOUND_TRUTH_PATH \
    --hyp $SAVE_DIR/test.output \
    --lang $TARGET \
    2>&1 | tee -a $RESULT_FILE;
echo "Evaluating compilation accuracy"
cd $CURRENT_DIR;
python $evaluator_script/compile.py \
    --input_file $SAVE_DIR/test.output \
    --language $TARGET \
    2>&1 | tee -a $RESULT_FILE;

count=`ls -1 *.class 2>/dev/null | wc -l`;
[[ $count != 0 ]] && rm *.class;

<<com
echo "Evaluating Execution Based Evaluation Accuracy"
cd $CURRENT_DIR;
python $evaluator_script/execution_evaluation_TC.py \
    --references $GOUND_TRUTH_PATH \
    --predictions $SAVE_DIR/test.output \
    --language $TARGET \
    --test_cases $TEST_CASES
com
}

function generate () {

MODEL_PATH=${SAVE_DIR}/checkpoint-best-ppl/pytorch_model.bin;
python run_gen.py \
    --do_generate \
    --model_type codet5 \
    --tokenizer_name roberta-base \
    --tokenizer_path $tokenizer_path \
    --model_name_or_path $pretrained_model \
    --task translate \
    --sub_task "${SOURCE}-${TARGET}" \
    --output_dir $SAVE_DIR \
    --data_dir $path_2_data \
    --cache_path $CACHE_DIR \
    --res_dir $SAVE_DIR \
    --eval_batch_size 4 \
    --max_source_length $source_length \
    --max_target_length $target_length \
    --beam_size 10 \
    --data_num -1 \
    2>&1 | tee ${SAVE_DIR}/generation_evaluation.log;
}

#train;
evaluate;
#generate;