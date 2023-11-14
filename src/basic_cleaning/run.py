#!/usr/bin/env python
"""
Download from W&B the raw dataset and apply some basic data cleaning, exporting the result to a new artifact
"""
import argparse
import logging
import wandb
import pandas as pd


logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):

    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    logging.info("Fatching artifact from wandb")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    dataframe = pd.read_csv(artifact_local_path)

    # remove outliers based on min_proce and max_price
    logging.info("remove outliers")
    idx = dataframe['price'].between(args.min_price, args.max_price)
    dataframe = dataframe[idx].copy()

    # saving dataframe
    logger.info("Save dataframe")
    dataframe.to_csv("clean_sample.csv", index=False)
    
    # upload clean data to wandb
    logger.info("upload clean data to wandb")

    artifact = wandb.Artifact(
        name=args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    logger.info("Artifact Name : %s", artifact.name)
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="A very basic data cleaning")


    parser.add_argument(
        "--input_artifact", 
        type=str,
        help="Name of the preprocessed artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str,
        help="Name of the resulted artifact",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str,
        help="output type",
        required=True
    )

    parser.add_argument(
        "--output_description", 
        type=str,
        help="output description",
        required=True
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float,
        help="Maximum price",
        required=True
    )


    args = parser.parse_args()

    go(args)
