ActiveRecord::Schema.define(version: 2023_10_27_000001) do

  create_table "links", force: :cascade do |t|
    t.string "url", null: false
    t.datetime "created_at", null: false
    t.datetime "updated_at", null: false
  end

end
