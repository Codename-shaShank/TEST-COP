class AddColumnsToLinks < ActiveRecord::Migration[7.0]
  def change
    add_column :links, :title, :string, if_not_exists: true
    add_column :links, :description, :string, if_not_exists: true
    add_column :links, :image, :string, if_not_exists: true
    add_column :links, :views_count, :integer, default: 0, if_not_exists: true
  end
end
