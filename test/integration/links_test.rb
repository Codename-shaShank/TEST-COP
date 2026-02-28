require "test_helper"

class LinksTest < ActionDispatch::IntegrationTest
  test "cannot create link without url" do
    post links_path, params: { link: { url: "" } }
    assert_response :unprocessable_entity
  end
end
