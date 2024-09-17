

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



num_comparisons = 25 # Comparing with Random and MostPop


# Loop through each CSV file
for (file in csv_files) {
  # Read the CSV file
  data <- read.csv(file)

  # Get the file name
  file_name <- basename(file)

  # Filter the columns by column name userID and AMF
  filtered_data <- data[, c("UserID", "ItemKNN", "UserKNN", "BPRMF",
                            "FunkSVD", "MF", "PMF", "PureSVD",
                            "Slim", "DeepFM", "NeuMF", "AMF",
                            "MultiVAE", "Random", "MostPop")]

  # Compute the mean for each algorithm
  means <- colMeans(filtered_data[, -1])  # Exclude UserID column

  # Convert means to strings with 3 decimals
  means <- formatC(means, format = "f", digits = 3)

  

  # Compute the paired t-test between
  #each column's value and the values from Random
  # Compute the paired t-test only if there is enough variability
  if (length(unique(filtered_data$Random)) > 1) {
    # Compute the paired t-test between each column's value and the values from Random
    p_values_random <- sapply(filtered_data[, -1], function(col) {
      t.test(col, filtered_data$Random, paired=TRUE)$p.value
    })
  } else {
    # If there's not enough variability, assign NA to p-values
    p_values_random <- rep(NA, length(colnames(filtered_data)) - 1)
  }

  # Compute the paired t-test between
  #each column's value and the values from Popularity
  # Compute the paired t-test only if there is enough variability
  if (length(unique(filtered_data$MostPop)) > 1) {
    # Compute the paired t-test between each column's value and the values from Random
    p_values_pop <- sapply(filtered_data[, -1], function(col) {
      t.test(col, filtered_data$MostPop, paired=TRUE)$p.value
    })
  } else {
    # If there's not enough variability, assign NA to p-values
    p_values_pop <- rep(NA, length(colnames(filtered_data)) - 1)
  }

    # Perform Bonferroni correction
  p_values_random_bonf <- p.adjust(p_values_random, method = "bonferroni", n = num_comparisons)
  p_values_pop_bonf <- p.adjust(p_values_pop, method = "bonferroni", n = num_comparisons)


  # Transform NA values in p_values_random into 1
  p_values_random_bonf[is.na(p_values_random_bonf)] <- 1
  p_values_pop_bonf[is.na(p_values_pop_bonf)] <- 1


  # Determine significant indices
  significant_indices <- p_values_random_bonf < 0.05

  # Add significance indicator to means
  means[significant_indices] <- paste0(means[significant_indices], "*")

  significant_indices <- p_values_pop_bonf < 0.05
  means[significant_indices] <- paste0(means[significant_indices], "$^{+}$")

  # Create a row with algorithm names and their means
  row <- c(file_name, means)

  # Create a new row with the column names as algorithm
  #and the p values as values
  new_random_row <- c(metric = file_name, p_values_random)


  if (is.null(algorithm_means)) {
    # If algorithm_means is NULL, initialize it with the first row
    algorithm_means <- data.frame(t(row), stringsAsFactors = FALSE)
    colnames(algorithm_means) <- c("metric",  "ItemKNN", "UserKNN", "BPRMF",
                                   "FunkSVD", "MF", "PMF", "PureSVD",
                                   "Slim", "DeepFM", "NeuMF", "AMF",
                                   "MultiVAE", "Random", "MostPop")

    algorithm_random_significance <- data.frame(t(new_random_row), stringsAsFactors = FALSE)
    colnames(algorithm_random_significance) <- c("metric",  "ItemKNN",
                                          "UserKNN", "BPRMF",
                                          "FunkSVD", "MF", "PMF", "PureSVD",
                                          "Slim", "DeepFM", "NeuMF", "AMF",
                                          "MultiVAE", "Random", "MostPop")

  } else {
    # Append the row to the algorithm_means data frame
    algorithm_means <- rbind(algorithm_means, row)
    algorithm_random_significance <- rbind(algorithm_random_significance, new_random_row)
  }
}


library(dplyr)

algorithm_means_goodreads <- algorithm_means %>%
  filter(grepl("^Goodreads", metric))

algorithm_means_ml <- algorithm_means %>%
  filter(grepl("^ML", metric))


algorithm_means_goodreads <- algorithm_means_goodreads %>%
  select(metric, Random, MostPop, ItemKNN, UserKNN, BPRMF, FunkSVD, MF, PMF, PureSVD,
         Slim, DeepFM, NeuMF, AMF, MultiVAE) %>%
  mutate(metric = ifelse(grepl("Goodreads_biasmeter_gender_HITS.csv", metric), 
  "HIT$_{BiasMeter, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_biasmeter_gender_MRRBAD.csv", metric), 
  "MRR$_{BiasMeter, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_biasmeter_gender_REC-ST.csv", metric), 
  "REC-ST$_{BiasMeter, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_biasmeter_race_HITS.csv", metric), 
  "HIT$_{BiasMeter, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_biasmeter_race_MRRBAD.csv", metric), 
  "MRR$_{BiasMeter, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_biasmeter_race_REC-ST.csv", metric), 
  "REC-ST$_{BiasMeter, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_biasmeter_religion_HITS.csv", metric), 
  "HIT$_{BiasMeter, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_biasmeter_religion_MRRBAD.csv", metric), 
  "MRR$_{BiasMeter, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_biasmeter_religion_REC-ST.csv", metric), 
  "REC-ST$_{BiasMeter, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_gpt35-turbo_gender_HITS.csv", metric), 
  "HIT$_{GPT, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_gpt35-turbo_gender_MRRBAD.csv", metric), 
  "MRR$_{GPT, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_gpt35-turbo_gender_REC-ST.csv", metric), 
  "REC-ST$_{GPT, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_gpt35-turbo_race_HITS.csv", metric), 
  "HIT$_{GPT, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_gpt35-turbo_race_MRRBAD.csv", metric), 
  "MRR$_{GPT, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_gpt35-turbo_race_REC-ST.csv", metric), 
  "REC-ST$_{GPT, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_gpt35-turbo_religion_HITS.csv", metric), 
  "HIT$_{GPT, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_gpt35-turbo_religion_MRRBAD.csv", metric), 
  "MRR$_{GPT, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_gpt35-turbo_religion_REC-ST.csv", metric), 
  "REC-ST$_{GPT, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_lexicon-model_gender_HITS.csv", metric), 
  "HIT$_{NGIM, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_lexicon-model_gender_MRRBAD.csv", metric), 
  "MRR$_{NGIM, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("Goodreads_lexicon-model_gender_REC-ST.csv", metric), 
  "REC-ST$_{NGIM, Gender}$", metric))




algorithm_means_ml <- algorithm_means_ml %>%
  select(metric, Random, MostPop, ItemKNN, UserKNN, BPRMF, FunkSVD, MF, PMF, PureSVD,
         Slim, DeepFM, NeuMF, AMF, MultiVAE) %>%
  mutate(metric = ifelse(grepl("ML-children_biasmeter_gender_HITS.csv", metric), 
  "HIT$_{BiasMeter, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_biasmeter_gender_MRRBAD.csv", metric), 
  "MRR$_{BiasMeter, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_biasmeter_gender_REC-ST.csv", metric), 
  "REC-ST$_{BiasMeter, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_biasmeter_race_HITS.csv", metric), 
  "HIT$_{BiasMeter, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_biasmeter_race_MRRBAD.csv", metric), 
  "MRR$_{BiasMeter, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_biasmeter_race_REC-ST.csv", metric), 
  "REC-ST$_{BiasMeter, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_biasmeter_religion_HITS.csv", metric), 
  "HIT$_{BiasMeter, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_biasmeter_religion_MRRBAD.csv", metric), 
  "MRR$_{BiasMeter, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_biasmeter_religion_REC-ST.csv", metric), 
  "REC-ST$_{BiasMeter, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_gpt35-turbo_gender_HITS.csv", metric), 
  "HIT$_{GPT, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_gpt35-turbo_gender_MRRBAD.csv", metric), 
  "MRR$_{GPT, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_gpt35-turbo_gender_REC-ST.csv", metric), 
  "REC-ST$_{GPT, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_gpt35-turbo_race_HITS.csv", metric), 
  "HIT$_{GPT, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_gpt35-turbo_race_MRRBAD.csv", metric), 
  "MRR$_{GPT, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_gpt35-turbo_race_REC-ST.csv", metric), 
  "REC-ST$_{GPT, Race}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_gpt35-turbo_religion_HITS.csv", metric), 
  "HIT$_{GPT, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_gpt35-turbo_religion_MRRBAD.csv", metric), 
  "MRR$_{GPT, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_gpt35-turbo_religion_REC-ST.csv", metric), 
  "REC-ST$_{GPT, Religion}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_lexicon-model_gender_HITS.csv", metric), 
  "HIT$_{NGIM, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_lexicon-model_gender_MRRBAD.csv", metric), 
  "MRR$_{NGIM, Gender}$", metric)) %>%
  mutate(metric = ifelse(grepl("ML-children_lexicon-model_gender_REC-ST.csv", metric), 
  "REC-ST$_{NGIM, Gender}$", metric))

# Define a function to format column names with \rotatebox
format_column_names <- function(column_names) {
  formatted_names <- sprintf("\\rotatebox[origin=c]{70}{%s}", column_names)
  return(formatted_names)
}

# Apply the formatting function to column names
column_names_goodreads <- format_column_names(colnames(algorithm_means_goodreads))
column_names_ml <- format_column_names(colnames(algorithm_means_ml))

# Assign the formatted column names
colnames(algorithm_means_goodreads) <- column_names_goodreads
colnames(algorithm_means_ml) <- column_names_ml

library(xtable)

# Convert algorithm_means_goodreads to LaTeX table
latex_table_goodreads <- xtable(algorithm_means_goodreads, caption="Goodreads", label="tab:goodreads")
print(latex_table_goodreads, type='latex', sanitize.text.function = identity, include.rownames=FALSE)

# Convert algorithm_means_ml to LaTeX table
latex_table_ml <- xtable(algorithm_means_ml, caption="MovieLens", label="tab:ml")
print(latex_table_ml, type='latex', sanitize.text.function = identity, include.rownames=FALSE)

