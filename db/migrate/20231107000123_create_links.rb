# This file appears to be causing the ActiveRecord::DuplicateMigrationNameError.
# Renaming the file with a unique timestamp to fix the duplication issue.

class CreateLinks < ActiveRecord::Migration[8.0]
  def change
    create_table :links do |t|
      t.string :url
      t.timestamps
    end
  end
end
