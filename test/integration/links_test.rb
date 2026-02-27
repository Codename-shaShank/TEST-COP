require "test_helper"

class LinksTest < ActionDispatch::IntegrationTest
  test "cannot create link without url" do
    # Check initial state
    assert_difference "Link.count", 0 do
      post links_path, params: { link: { url: "" } }
    end

    assert_response :unprocessable_entity
    assert_match /can't be blank/, response.body
  end
end
