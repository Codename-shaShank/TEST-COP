class LinksController < ApplicationController
  def create
    @link = Link.new(link_params)
    if @link.save
      redirect_to @link, notice: 'Link was successfully created.'
    else
      render :new, status: :unprocessable_entity
    end
  end

  private

  def link_params
    params.require(:link).permit(:url)
  end
end
