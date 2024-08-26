library(ggplot2)  
library(dplyr)
library(reshape2)  # For melt function
library(tidyverse)
library(ggpubr)
library(rstatix)


# Set the root directory
root_dir <- "../Results/SDM"

# Function to recursively find all CSV files
find_csv_files <- function(directory) {
  file_list <- list.files(directory, recursive = TRUE, full.names = TRUE)
  csv_files <- file_list[grepl(".csv$", file_list) & !grepl("(gender.csv$|race.csv$|religion.csv$)", file_list)]
  return(csv_files)
}

# Get all CSV files
csv_files <- find_csv_files(root_dir)

# Read each CSV file and save their names
file_names <- c()
# Initialize algorithm_means as NULL
algorithm_means <- NULL
algorithm_random_significance <- NULL
algorithm_pop_significance <- NULL



# Set the comparisons to be made
dataset_to_test = "ML-children" # Goodreads, ML-children
stereotype_to_test = c("religion", "race", "gender")
SDM_to_test = "biasmeter" # lexicon-model, biasmeter, chatgpt
metric_to_test = "HITS" #MRRBAD, HITS, REC-ST

df <- data.frame(UserID = numeric(),
                       stereotype = character(),
                       algorithm = character(),
                       score = numeric(),
                       stringsAsFactors = FALSE)


# Loop through each CSV file
for (file in csv_files) {
  
  # Read the CSV file
  data <- read.csv(file)

  # Get the file name
  file_name <- basename(file)



  # Split the file name at "_"
  file_name <- strsplit(file_name, "\\.")[[1]]
  file_name_parts <- strsplit(file_name, "_")[[1]]

  # Extract the relevant parts from the file name
  dataset <- file_name_parts[1]
  SDM <- file_name_parts[2]
  stereotype <- file_name_parts[3]
  metric <- file_name_parts[4]
  


  if (dataset == dataset_to_test & SDM == SDM_to_test & metric == metric_to_test & stereotype %in% stereotype_to_test) {
    
    if (dataset_to_test == "Goodreads") {
      num_comparisons <- 78
          # Filter the columns by column name userID and AMF
    filtered_data <- data[, c("UserID", "Random", "MostPop", 
                              "ItemKNN", "UserKNN",
                               "BPRMF",
                              "FunkSVD", "MF", "PMF", "PureSVD",
                              "Slim", "DeepFM", "NeuMF", "AMF",
                              "MultiVAE")]
    } else if (dataset_to_test == "ML-children") {
      num_comparisons <- 91
          # Filter the columns by column name userID and AMF
    filtered_data <- data[, c("UserID", "Random", "MostPop", 
                              "ItemKNN", "UserKNN",
                              "VSM", "BPRMF",
                              "FunkSVD", "MF", "PMF", "PureSVD",
                              "Slim", "DeepFM", "NeuMF", "AMF",
                              "MultiVAE")]
    }


    melted_df <- melt(filtered_data, id.vars = c("UserID"))

    # rename column variable to algorithm
    melted_df <- melted_df %>% 
              rename(algorithm = variable,
                     score = value)
    
    melted_df$stereotype <- stereotype

    # Append the melted_df to the df
    df <- rbind(df, melted_df)
  }
}



# Two way Anova
df %>%
  group_by(stereotype) %>%
  get_summary_stats(score, type = "mean_sd")


#df %>%
#  group_by(algorithm, stereotype) %>%
#  identify_outliers(score)


#df %>%
#  group_by(algorithm, stereotype) %>%
#  shapiro_test(score)


res.aov <- anova_test(
  data = df, dv = score, wid = UserID,
  within = c(algorithm, stereotype)
  )
get_anova_table(res.aov)



pwc <- df %>%
  pairwise_t_test(
    score ~ stereotype, paired = TRUE,
    p.adjust.method = "bonferroni"
    )
pwc